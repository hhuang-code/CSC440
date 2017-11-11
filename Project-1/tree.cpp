#include <algorithm>
#include <iostream>
using namespace std;

#include "tree.hpp"

tree::tree(int ams){
	root = new tree_node("ROOT", nullptr);
	abs_min_sup = ams;
	header_table.clear();
	freq_of_item.clear();
}

void tree::build_freq_of_item(DATABASE& db){
	map<ITEM, int> tmp_cnt;
	for(TRANS trans : db){
		for(ITEM item : trans){
			tmp_cnt[item]++;
		}
	}

	for(map<ITEM, int>::const_iterator iter = tmp_cnt.cbegin(); iter != tmp_cnt.end(); iter++){
		if((*iter).second < abs_min_sup){
			tmp_cnt.erase(iter);
		}
	}

	for(pair<ITEM, int> pair : tmp_cnt){
		freq_of_item.insert(pair);
	}
}

void tree::build_tree(DATABASE& db){
	// Check every transaction
	for(TRANS trans : db){
		tree_node* cur_ptr = root;
		for(const pair<ITEM, int>& pair : freq_of_item){
			ITEM item = pair.first;
			// Find one item in this transaction
			if(find(trans.cbegin(), trans.cend(), item) != trans.cend()){
				// Check if this item has been added to fp_tree
				vector<tree_node*>::const_iterator find_ptr = cur_ptr->children.cbegin();
				for(; find_ptr != cur_ptr->children.cend(); find_ptr++){
					if((*find_ptr)->item == item){
						break;
					}
				}

				// The item node exists, increase its frequency by one
				if(find_ptr != cur_ptr->children.cend()){
					tree_node* cur_child_ptr = *find_ptr;
					cur_child_ptr->freq += 1;
					cur_ptr = cur_child_ptr;
				}else{	// The item node does not exist, create a new one
					tree_node* new_child_ptr = new tree_node(item, cur_ptr);
					cur_ptr->children.push_back(new_child_ptr);
					// Update header_table
					if(header_table.count(new_child_ptr->item)){	// This item exists in the header_table
						tree_node* cur_table_ptr = header_table[new_child_ptr->item];
						while(cur_table_ptr->next_node){
							cur_table_ptr = cur_table_ptr->next_node;
						}
						cur_table_ptr->next_node = new_child_ptr;
					}else{	// This item does not exists in the header_table
						header_table[new_child_ptr->item] = new_child_ptr;
					}
					cur_ptr = new_child_ptr;
				}
			}// end if
		}// end for transaction
	}// end for db
}

bool tree::is_empty() const {
	if(root != nullptr && root->children.size() != 0){
		return false;
	}else{
		return true;
	}
}

bool tree::is_single_path() const {
	return is_empty() || root->single_children_path();
}

// Helper function
void tree::display_freq_of_item(){
	for(const pair<ITEM, int>& pair : freq_of_item){
		cout << pair.first << " " << pair.second << endl;
	}
}