class bigNum
{
private:
	//Hidden elements and functions
	int base;
	int* bigNumArr;
	int bigNumArrSize;
	char bigNumSign;

	int* fileRead(char* fileIn, int base, int& arrSize, char& numberSign);
	bool fileWrite(int* bigNumArr, char numSign, int bigNumArrSize, char* fileResultName, int base);
	char resultSign(char operation, char firstNumSign, char secNumSign, int* firstNumArr, int* secNumArr, int firstNumArrSize, int secNumArrSize);
	void findMaxMin(int* firstNumArr, int* secNumArr, int firstNumArrSize, int secNumArrSize, int** maxNumArr, int** minNumArr, int& maxNumArrSize, int& minNumArrSize);
	int* withoutNulls(int* arrWithNulls, int& arrSize);
	int* longToInt(long long int ArrElem, int* longToIntArr, int& longToIntArrSize, int base);
	int* copyArr(int* newArr, int* oldArr, int& newArrSize, int oldArrSize);

	void copyBigNum(const bigNum& rhv);
	int* shiftLeft(int* arrForShift, int& arrSize);

	//Arithmetic operation
	bigNum& sumOrSub(const bigNum& lhv, const bigNum& rhv, bool isSub, char tmpSecSign);
	
	int* addition(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, int base);
	int* substraction(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, int base);
	int* multiplication(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, int base);
	int* divOnDigit(int* firstNumArr, int digit, int* resNumArr, int firstNumArrSize, int& resNumArrSize, int& tail, bool isRem, int base);
	int* dividing(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, bool isRem, int base);
	int* dividing2(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, bool isRem, int base);
	int* involution(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, int base);
	int* remainder(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, int base);

public:
	//Constructor
	bigNum();
	bigNum(const char* string);
	
	int getInt();

	//Destructor
	~bigNum();

	//operators overloading
	bigNum& operator=(const bigNum& rv);
	bigNum& operator+(const bigNum& rv);
	bigNum& operator-(const bigNum& rv);
	bigNum& operator*(const bigNum& rv);
	bigNum& operator/(const bigNum& rv);
	bigNum& operator^(const bigNum& rv);
	bigNum& operator%(const bigNum& rv);
	bool operator==(const bigNum& rv);
	bool operator!=(const bigNum& rv);
	bool operator>=(const bigNum& rv);
	bool operator<=(const bigNum& rv);
	bool operator>(const bigNum& rv);
	bool operator<(const bigNum& rv);

	//Other functions
	bool Read(char* inFileName, int base);
	bool Write(char* outFileName);
};