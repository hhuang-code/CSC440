#include <iostream>
#include <fstream>

using namespace std;

#include "database.hpp"

vector<string> attr_name = {"age", "workclass", "fnlwgt", "education", "education-num", "marital-status", "occupation", 
							"relationship", "race", "sex", "capital-gain", "capital-loss", "hours-per-week", "native-country", "income"};

// Delete leading and tailing whitespace.
string trim(const string& str){
	const auto pos1 = str.find_first_not_of(' ');
	if(pos1 == string::npos){
		return "";
	}else{
		const auto pos2 = str.find_last_not_of(' ');
		const auto len = pos2 - pos1 + 1;

		return str.substr(pos1, len);
	}
}

// Split s by c.
void split(const string& s, vector<string>& v, const string& c){
    string::size_type pos1, pos2;
    pos1 = 0;
    pos2 = s.find(c);
    while(pos2 != string::npos){
        v.push_back(s.substr(pos1, pos2 - pos1));
        pos1 = pos2 + c.size();
        pos2 = s.find(c, pos1);
    }
    if(pos1 != s.length()){
        v.push_back(s.substr(pos1));
    }
}

// Read file and load dataset
DATABASE load_data(string filename){
	DATABASE db;
	vector<string> tmp_vec;

	ifstream file(filename);
	if(!file){
		cout << "Cannot open " << filename << "!" << endl;
		exit(1);
	}else{
		string line;
		while(getline(file, line)){
			if(trim(line) != ""){
				TRANS trans;
				tmp_vec.erase(tmp_vec.begin(), tmp_vec.end());
				split(line, tmp_vec, ",");
				for(int i = 0; i < tmp_vec.size(); i++){
					ITEM item = attr_name[i] + ":" + trim(tmp_vec[i]);
					//ITEM item = trim(tmp_vec[i]);
					trans.insert(item);
				}
				db.push_back(trans);
			}else{
				continue;
			}
		}
	}

	return db;
}
