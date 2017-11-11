#include <iostream>
#include <algorithm>
#include <cmath>
using namespace std;

#include <pthread.h>

#include "database.hpp"

// Used to passing arguments to threads.
struct Params{
	const DATABASE* sub_db;
	float min_sup;
};

// Store final results
LSET final_res;

// A lock for thread syncronization
pthread_mutex_t lock;

// Generate candidate 1-itemsets (C1 set)
CSET im_generate_c1_set(DATABASE& db){
	CSET c1_set;

	// Scan all transactions in the database
	for(TRANS& trans : db){
		for(ITEM item : trans){
			ITEMSET itemset;
			itemset.insert(item);
			if(c1_set.find(itemset) != c1_set.end()){
				c1_set[itemset]++;
			}else{
				c1_set[itemset] = 1;
			}
		}
	}

	return c1_set;
}

/*
	Generate frequent 1-itemset (L1 set)
	min_sup: relative support (0 < min_sup < 1); minimal absolute support = min_sup * db.size()
*/
LSET im_generate_l1_set(CSET& c1_set, const DATABASE& db, float min_sup){
	int abs_min_sup = ceil(min_sup * db.size());
	LSET l1_set(c1_set);
	for(const pair<ITEMSET, int>& itemset : l1_set){
		if(itemset.second < abs_min_sup){
			l1_set.erase(itemset.first);
		}
	}

	return l1_set;
}

/*
	Check if a candidate k-itemset has infrequent subset.
	The input itemset has (k) items and lset is a L(k - 1)-set 
*/
bool im_has_infrequent_subset(ITEMSET itemset, LSET lset){
	for(const ITEM& item : itemset){
		ITEMSET tmp_itemset(itemset);
		tmp_itemset.erase(item);
		if(lset.find(tmp_itemset) == lset.end()){
			return true;
		}else{
			continue;
		}
	}

	return false;
}

// Generate Ck-set from L(k-1)-set, where k >= 2
CSET im_apriori_gen(LSET lset){
	CSET cset;
		LSET::iterator iter1, iter2;
		for(iter1 = lset.begin(); iter1 != lset.end(); iter1++){
			for(iter2 = next(iter1, 1); iter2 != lset.end(); iter2++){
				if(equal((iter1->first).begin(), prev((iter1->first).end(), 2), (iter2->first).begin()) && *((iter1->first).rbegin()) != *((iter2->first).rbegin())){
					// Join two itemsets
					ITEMSET new_itemset(iter1->first);
					new_itemset.insert((iter2->first).begin(), (iter2->first).end());
					if(im_has_infrequent_subset(new_itemset, lset)){
						continue;
					}else{
						cset[new_itemset] = 0;
					}
				}
			}
		}
	return cset;
}

// If an itemset int cset is contained in a transaction, its count increases by 1.
void im_get_cset_count(DATABASE& db, CSET& cset){
	for(auto& itemset : cset){
		for(TRANS& trans : db){
			if(includes(trans.begin(), trans.end(), (itemset.first.begin()), (itemset.first.end()))){
				itemset.second += 1;
			}
		}
	}
}

/*
	Generate all frequent itemsets.
	min_sup: relative support (0 < min_sup < 1); minimal absolute support = min_sup * db.size()
*/
/*vector<LSET> im_sub_apriori_alg(DATABASE& db, float min_sup){*/
void* im_sub_apriori_alg(void* params){
	struct Params* p = static_cast<Params*>(params);
	DATABASE db = *(p->sub_db);
	float min_sup = p->min_sup;
	int abs_min_sup = ceil(min_sup * db.size());

	CSET c1_set = im_generate_c1_set(db);
	LSET l1_set = im_generate_l1_set(c1_set, db, min_sup);
	vector<LSET> sub_res;
	sub_res.push_back(l1_set);
	LSET lset;
	bool is_l1 = true;
	while(true){
		if(is_l1){
			lset = l1_set;
			is_l1 = false;
		}
		CSET cset = im_apriori_gen(lset);
		lset.clear();
		if(cset.size() > 0){	
			im_get_cset_count(db, cset);	// Get the count of every item in C set
			for(const pair<ITEMSET, int>& p : cset){
				if(p.second >= abs_min_sup){
					lset[p.first] = p.second;
				}
			}
			if(lset.size() > 0){
				sub_res.push_back(lset);
			}else{
				break;
			}
		}else{
			break;
		}
	}

	// Combine local results to global candidates
	pthread_mutex_lock(&lock);
	for(map<ITEMSET, int>& m : sub_res){
		for(pair<ITEMSET, int> p : m){
			if(final_res.find(p.first) != final_res.end()){
				final_res[p.first] += p.second;
			}else{
				final_res[p.first] = p.second;
			}
		}
	}
	pthread_mutex_unlock(&lock);

	pthread_exit(NULL);
}

LSET im_apriori_alg(DATABASE& db, float min_sup, int num_of_partition){
	int db_size = db.size();
	int tmp_num = num_of_partition;
	
	// Partition the original database into different non-overlapped parts
	int partition_size = db_size / num_of_partition;
	set<DATABASE> sub_dbs;
	DATABASE::iterator from = db.begin();
	while(tmp_num > 1){
		DATABASE sub_db;
		sub_db.assign(from, from + partition_size);
		from += partition_size;
		tmp_num--;
		sub_dbs.insert(sub_db);
	}
	DATABASE last_sub_db;
	last_sub_db.assign(from, db.end());
	sub_dbs.insert(last_sub_db);

	// Create threads to run Apriori on each partition
	vector<vector<LSET> > res;
	set<DATABASE>::iterator iter = sub_dbs.begin();

	if(pthread_mutex_init(&lock, NULL) != 0){
		cout << "Mutex initialization failed. " << 
		"The running result maybe incorrect." << endl;
	}

	pthread_t tid[num_of_partition];
	for(int i = 0; i < num_of_partition; i++){
		Params params;
		params.sub_db = &(*iter);
		params.min_sup = min_sup;
		int err = pthread_create(&tid[i], NULL, im_sub_apriori_alg, &params);
		if(err != 0){
			cout << "Cannot create " << i + 1 << " -th thread." << endl;
		}
		iter++;
	}

	for(int i = 0; i < num_of_partition; i++){
		pthread_join(tid[i], NULL);
	}

	pthread_mutex_destroy(&lock);

	/* 
		Second scan to remove some candidates
		Actually, since we have calculated the accumulated support count 
		during each thread, we just have to check the support count
	*/
	int abs_min_sup = ceil(min_sup * db.size());
	for(const pair<ITEMSET, int>& p : final_res){
		if(p.second < abs_min_sup){
			final_res.erase(p.first);
		}
	}

	return final_res;
}