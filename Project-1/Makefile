test: test.o loaddata.o apriori.o fpgrowth.o tree.o tree_node.o improved_apriori.o
	g++  -pthread -o test test.o loaddata.o apriori.o fpgrowth.o tree.o tree_node.o improved_apriori.o

clean:
	rm *.o test

loaddata.o: loaddata.cpp database.hpp
	g++ -c loaddata.cpp

apriori.o: apriori.cpp database.hpp
	g++ -c apriori.cpp

tree.o: tree.cpp tree.hpp database.hpp
	g++ -c tree.cpp

tree_node.o: tree_node.cpp tree_node.hpp database.hpp
	g++ -c tree_node.cpp

fpgrowth.o: fpgrowth.cpp database.hpp tree.hpp tree_node.hpp
	g++ -c fpgrowth.cpp tree.cpp tree_node.cpp

improved_apriori: improved_apriori.cpp database.hpp
	g++ -c improved_apriori.cpp

test.o: test.cpp database.hpp
	g++ -c test.cpp