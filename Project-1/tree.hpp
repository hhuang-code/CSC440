#ifndef TREE_H
#define TREE_H

#include <vector>
#include <map>

using namespace std;

#include "tree_node.hpp"
#include "database.hpp"

/* 
	Order by the second element in a pair by decreasing order.
	If the second elements are the same, order by the first element in increasing order.
*/
struct decrease_order_comp{
	bool operator() (const pair<ITEM, int>& left, const pair<ITEM, int>& right) const{
		return (left.second > right.second) || (!(left.second > right.second) && left.first < right.first);
	} 
};

class tree{
public:
	tree_node* root;
	int abs_min_sup;	// absolute minimal support = (relative minimal support) * (total number of db)
	set<pair<ITEM, int>, decrease_order_comp> freq_of_item;	// keep items of frequency not less than abs_min_sup, in descreasing order 
	map<ITEM, tree_node*> header_table;
	
	tree(int ams);
	void build_freq_of_item(DATABASE& db);
	void build_tree(DATABASE& db);
	bool is_empty() const;
	bool is_single_path() const;

	// Helper function
	void display_freq_of_item();
};

#endif