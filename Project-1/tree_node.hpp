#ifndef TREE_NODE_H
#define TREE_NODE_H

#include <string>
#include <set>

using namespace std;

#include "database.hpp"

class tree_node{
public:
	ITEM item;
	int freq;
	tree_node* parent;
	tree_node* next_node;	// Used in header table
	vector<tree_node*> children;

	tree_node(ITEM it, tree_node* p);
	bool single_children_path() const;	// Check if this node has a single children path
};

#endif