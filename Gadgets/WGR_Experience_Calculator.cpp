// This file is used to calculate the experience required after lv.100 in WGR

#include <iostream>
#include <cmath>

int experienceCalculate(int a);

//g++ -std=c++11 your_file.cpp -o your_program

int main(int argc, char* argv[])
{
	// std::string::size_type sz;
	// int inputA = stoi(argv[1], &sz);
	// int nextLevel = inputA + 1;
	// int result = experienceCalculate(inputA);
	// cout << "The amount of experience required from lv." << inputA << " to lv."
	// 	 << nextLevel << " is " << result << endl;

	int nextLevel, result;
	for (int i = 125; i < 160; i++)
	{
		nextLevel = i + 1;
		result = experienceCalculate(i);
		std::cout << "The amount of experience required from lv." << i << " to lv."
			 << nextLevel << " is " << result << std::endl;
	}

	return 0;
}

int experienceCalculate(int a)
{
	return (20 * pow(a, 2) + 60 * a - 160000);
}