#include <iostream>
#include <algorithm>
#include <cmath>


#include "database.hpp"

// Generate candidate 1-itemsets (C1 set)
CSET generate_c1_set(DATABASE& db){
	CSET c1_set;

	// Scan all transactions in the database
	DATABASE::iterator db_iter = db.begin();
	for(; db_iter != db.end(); db_iter++){
		// Scan all items in a single transaction
		TRANS::iterator trans_iter = db_iter->begin();
		for(; trans_iter != db_iter->end(); trans_iter++){
			ITEMSET itemset;
			itemset.insert(*trans_iter);
			// ATTENTION: since all itemset here contains the same number of items, find() function will function well
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
LSET generate_l1_set(CSET& c1_set, const DATABASE& db, float min_sup){
	int trans_num = db.size();
	int abs_min_sup = ceil(min_sup * trans_num);
	LSET l1_set(c1_set);
	CSET::iterator iter = l1_set.begin();
	for(; iter != l1_set.end(); iter++){
		if(iter->second < abs_min_sup){
			l1_set.erase(iter);
		}
	}

	return l1_set; 
}

// Display candidate set (C set) or frequent set (L set)
void display_corl_set(CSET& cset){
	// Traverse all itemsets in cset
	CSET::iterator set_iter = cset.begin();
	for(; set_iter != cset.end(); set_iter++){
		//Traverse all items in a single itemset
		ITEMSET::iterator item_set = (set_iter->first).begin();
		cout << "{ ";
		for(; item_set != (set_iter->first).end(); item_set++){
			cout << *item_set << " ";
		}
		cout << "} : " << set_iter->second << endl;
	}
}

/*
	Check if a candidate k-itemset has infrequent subset.
	The input itemset has (k) items and lset is a L(k - 1)-set 
*/
bool has_infrequent_subset(ITEMSET itemset, LSET lset){
	ITEMSET::iterator iter = itemset.begin();
	for(; iter != itemset.end(); iter++){
		ITEMSET tmp_itemset(itemset);
		tmp_itemset.erase(*iter);
		if(lset.find(tmp_itemset) == lset.end()){
			return true;
		}else{
			continue;
		}
	}

	return false;
}

/*
	Generate Ck-set from L(k-1)-set, where k >= 2
*/
CSET apriori_gen(LSET lset){
	CSET cset;
	LSET::iterator iter1, iter2;
	for(iter1 = lset.begin(); iter1 != lset.end(); iter1++){
		for(iter2 = next(iter1, 1); iter2 != lset.end(); iter2++){
			if(equal((iter1->first).begin(), prev((iter1->first).end(), 2), (iter2->first).begin()) && *((iter1->first).rbegin()) != *((iter2->first).rbegin())){
				// Join two itemsets
				ITEMSET new_itemset(iter1->first);
				new_itemset.insert((iter2->first).begin(), (iter2->first).end());
				if(has_infrequent_subset(new_itemset, lset)){
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
void get_cset_count(DATABASE& db, CSET& cset){
	DATABASE::iterator db_iter;

	CSET::iterator citer = cset.begin();
	for(; citer != cset.end(); citer++){
		for(db_iter = db.begin(); db_iter != db.end(); db_iter++){
			if(includes(db_iter->begin(), db_iter->end(), (citer->first).begin(), (citer->first).end())){
				citer->second = citer->second + 1;
			}
		}
	}
}

/*
	Generate all frequent itemsets.
	min_sup: relative support (0 < min_sup < 1); minimal absolute support = min_sup * db.size()
*/
vector<LSET> apriori_alg(DATABASE& db, float min_sup){
	int trans_num = db.size();
	int abs_min_sup = ceil(min_sup * trans_num);

	CSET c1_set = generate_c1_set(db);
	LSET l1_set = generate_l1_set(c1_set, db, min_sup);
	vector<LSET> res;
	res.push_back(l1_set);
	LSET lset;
	bool is_l1 = true;
	while(true){
		if(is_l1){
			lset = l1_set;
			is_l1 = false;
		}
		CSET cset = apriori_gen(lset);
		lset.clear();
		if(cset.size() > 0){
			get_cset_count(db, cset);	// Get the count of every item in C set
			CSET::iterator citer = cset.begin();
			for(; citer != cset.end(); citer++){
				if(citer->second >= abs_min_sup){
					lset[citer->first] = citer->second;
				}
			}
			if(lset.size() > 0){
				res.push_back(lset);
			}else{
				break;
			}
		}else{
			break;
		}
	};

	return res;
}
