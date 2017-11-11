#ifndef DATABASE_HPP
#define DATABASE_HPP

#include <string>
#include <vector>
#include <set>
#include <map>

using namespace std;

// Following are used by both Apriori and FP-growth
typedef string ITEM;
typedef set<ITEM> TRANS;
typedef set<ITEM> ITEMSET;	// Both transactions and itemsets consist of the same elements: items (represented by string)
typedef vector<TRANS> DATABASE;
extern DATABASE load_data(string filename);

// Following are used by Apriori and Improved Apriori exclusively
typedef map<ITEMSET, int> CSET;	// Candidate set
typedef map<ITEMSET, int> LSET;	// Frequent set
extern vector<LSET> apriori_alg(DATABASE& db, float min_sup);
extern LSET im_apriori_alg(DATABASE& db, float min_sup, int num_of_partition);
extern void display_corl_set(CSET& cset);

// Following are used by FP-growth exculsively
typedef vector<pair<ITEMSET, int> > CPBASE;	// Conditional pattern base
typedef set<pair<ITEMSET, int> > FSET;	// Frequent set (used by fp-growth)
extern FSET fp_growth_alg(DATABASE& db, float min_sup);
extern void display_fset(FSET& fset);

#endif