#include "tree_node.hpp"

tree_node::tree_node(ITEM it, tree_node* p){
	item = it; 
	freq = 1;
	parent = p;
	next_node = nullptr;
	children.clear();
}

bool tree_node::single_children_path() const {
	if(children.size() == 0){
		return true;
	}else if(children.size() > 1){
		return false;
	}else{
		return (children.front())->single_children_path();	// children.size() == 1
	}
}