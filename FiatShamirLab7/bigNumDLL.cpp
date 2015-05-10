#include <stdio.h>
#include <math.h>
#include "bigNumDLL.h"
#include <string.h>
#include <stdlib.h>
#include <time.h>

bigNum::bigNum()
{
	bigNumArr = NULL;
	bigNumArrSize = 0;
	bigNumSign = '\0';
	base = 0;
}

bigNum::bigNum(const char* string)
{
	int stringSize = strlen(string);
	int curPos = 0;

	if (string[0] == '-')
	{
		this->bigNumSign = '-';
		curPos = stringSize;
		stringSize -= 1;
	}
	else
	{
		this->bigNumSign = '+';
		curPos = stringSize;
	}

	this->base = 1000000000;
	if (!(stringSize % 9))
	{
		this->bigNumArrSize = stringSize / 9;
	}
	else
	{
		this->bigNumArrSize = (stringSize / 9 + 1);
	}

	this->bigNumArr = new int[this->bigNumArrSize];
	for (int i = 0; i < this->bigNumArrSize; i++)
	{
		this->bigNumArr[i] = 0;
	}

	for (int i = this->bigNumArrSize; i > 0; i--)
	{
		if ((curPos - 9) > 0)
		{
			curPos -= 9;
			for (int j = 0; j < 9; j++)
			{
				this->bigNumArr[i - 1] += (string[curPos + j] - 48)*(int)(pow((double)10, (9 - j - 1)));
			}
		}
		else
		{
			if (string[0] == '-')
			{
				for (int j = 1; j < curPos; j++)
				{
					this->bigNumArr[i - 1] += (string[j] - 48)*(int)(pow((double)10, (curPos - j - 1)));
				}
			}
			else
			{
				for (int j = 0; j < curPos; j++)
				{
					this->bigNumArr[i - 1] += (string[j] - 48)*(int)(pow((double)10, (curPos - j - 1)));
				}
			}
		}
	}
}

int bigNum::getInt()
{
	if (this->bigNumArrSize != 1)
	{
		return -1;
	}

	int value = this->bigNumArr[0];
	if (this->bigNumSign == '-')
	{
		value *= -1;
	}
	return value;
}

void bigNum::getRandBigNum(int bitsLen)
{	
	srand(time(NULL));
	if (!(bitsLen % 32))
	{
		bigNumArrSize = bitsLen / 32;
	}
	else
	{
		bigNumArrSize = bitsLen / 32 + 1;
	}
	
	base = 1000000000;
	bigNumSign = '+';
	
	if(bigNumArr)
	{
		delete[] bigNumArr;
	}
	bigNumArr = new int[bigNumArrSize];
	
	for(int i = 0; i < bigNumArrSize; i++)
	{
		bigNumArr[i] = (rand() * rand()) % base + 1;
	}
}

bigNum::~bigNum()
{
	if (this->bigNumArr)
	{
		delete[] this->bigNumArr;
	}
}

bigNum& bigNum::operator=(const bigNum& rv)
{
	if (this->bigNumArr)
	{
		delete[] this->bigNumArr;
	}

	copyBigNum(rv);
	return *this;
}

bigNum& bigNum::operator+(const bigNum& rv)
{
	return sumOrSub(*this, rv, false, rv.bigNumSign);
}

bigNum& bigNum::operator-(const bigNum& rv)
{
	char tmpSecSign = '\0';
	if (rv.bigNumSign == '-')
	{
		tmpSecSign = '+';
	}

	else
	{
		tmpSecSign = '-';
	}

	return sumOrSub(*this, rv, true, tmpSecSign);
}

bigNum& bigNum::operator*(const bigNum& rv)
{
	bigNum* resultNum = new bigNum;
	resultNum->bigNumSign = resultSign('*', this->bigNumSign, rv.bigNumSign, this->bigNumArr, rv.bigNumArr, this->bigNumArrSize, rv.bigNumArrSize);
	resultNum->base = this->base;
	resultNum->bigNumArr = multiplication(this->bigNumArr, rv.bigNumArr, resultNum->bigNumArr, this->bigNumArrSize, rv.bigNumArrSize, resultNum->bigNumArrSize, resultNum->base);
	return *resultNum;
}

bigNum& bigNum::operator/(const bigNum& rv)
{
	bigNum* resultNum = new bigNum;
	resultNum->bigNumSign = resultSign('/', this->bigNumSign, rv.bigNumSign, this->bigNumArr, rv.bigNumArr, this->bigNumArrSize, rv.bigNumArrSize);
	resultNum->base = this->base;
	resultNum->bigNumArr = dividing(this->bigNumArr, rv.bigNumArr, resultNum->bigNumArr, this->bigNumArrSize, rv.bigNumArrSize, resultNum->bigNumArrSize, false, resultNum->base);
	return *resultNum;
}

bigNum& bigNum::operator^(const bigNum& rv)
{
	if (rv.bigNumSign == '-')
	{
		printf("Power can't be negative! Error!\n");
		return *this;
	}

	bigNum* resultNum = new bigNum;
	resultNum->bigNumSign = this->bigNumSign;
	resultNum->base = this->base;
	resultNum->bigNumArr = involution(this->bigNumArr, rv.bigNumArr, resultNum->bigNumArr, this->bigNumArrSize, rv.bigNumArrSize, resultNum->bigNumArrSize, resultNum->base);
	return *resultNum;
}

bigNum& bigNum::operator%(const bigNum& rv)
{
	if (rv.bigNumSign == '-')
	{
		printf("Modul should be positive! Error!\n");
		return *this;
	}

	bigNum* resultNum = new bigNum;
	resultNum->bigNumSign = this->bigNumSign;
	resultNum->base = this->base;
	resultNum->bigNumArr = remainder(this->bigNumArr, rv.bigNumArr, resultNum->bigNumArr, this->bigNumArrSize, rv.bigNumArrSize, resultNum->bigNumArrSize, resultNum->base);
	if (resultNum->bigNumSign == '-')
	{
		*resultNum = sumOrSub(*resultNum, rv, false, '+');
		resultNum->bigNumSign = '+';
		resultNum->bigNumArr = remainder(resultNum->bigNumArr, rv.bigNumArr, resultNum->bigNumArr, resultNum->bigNumArrSize, rv.bigNumArrSize, resultNum->bigNumArrSize, resultNum->base);
	}
	return *resultNum;
}

bool bigNum::operator==(const bigNum& rv)
{
	if (resultSign('+', this->bigNumSign, rv.bigNumSign, this->bigNumArr, rv.bigNumArr, this->bigNumArrSize, rv.bigNumArrSize) == '=')
	{
		return true;
	}

	return false;
}

bool bigNum::operator!=(const bigNum& rv)
{
	if (resultSign('+', this->bigNumSign, rv.bigNumSign, this->bigNumArr, rv.bigNumArr, this->bigNumArrSize, rv.bigNumArrSize) == '=')
	{
		return false;
	}

	return true;
}

bool bigNum::operator>=(const bigNum& rv)
{
	char tempSecSign = '\0';

	if (rv.bigNumSign == '+')
	{
		tempSecSign = '-';
	}
	else
	{
		tempSecSign = '+';
	}

	if (resultSign('+', this->bigNumSign, tempSecSign, this->bigNumArr, rv.bigNumArr, this->bigNumArrSize, rv.bigNumArrSize) == '-')
	{
		return false;
	}

	return true;
}

bool bigNum::operator<=(const bigNum& rv)
{
	char tempSecSign = '\0';

	if (rv.bigNumSign == '+')
	{
		tempSecSign = '-';
	}
	else
	{
		tempSecSign = '+';
	}

	if (resultSign('+', this->bigNumSign, tempSecSign, this->bigNumArr, rv.bigNumArr, this->bigNumArrSize, rv.bigNumArrSize) == '+')
	{
		return false;
	}

	return true;
}

bool bigNum::operator>(const bigNum& rv)
{
	char tempSecSign = '\0';

	if (rv.bigNumSign == '+')
	{
		tempSecSign = '-';
	}
	else
	{
		tempSecSign = '+';
	}

	if (resultSign('+', this->bigNumSign, tempSecSign, this->bigNumArr, rv.bigNumArr, this->bigNumArrSize, rv.bigNumArrSize) == '+')
	{
		return true;
	}

	return false;
}

bool bigNum::operator<(const bigNum& rv)
{
	char tempSecSign = '\0';

	if (rv.bigNumSign == '+')
	{
		tempSecSign = '-';
	}
	else
	{
		tempSecSign = '+';
	}

	if (resultSign('+', this->bigNumSign, tempSecSign, this->bigNumArr, rv.bigNumArr, this->bigNumArrSize, rv.bigNumArrSize) == '-')
	{
		return true;
	}

	return false;
}

bool bigNum::Read(char* inFileName, int base)
{
	bigNumArr = fileRead(inFileName, base, bigNum::bigNumArrSize, bigNum::bigNumSign);
	if (!bigNumArr)
	{
		return false;
	}
	bigNum::base = base;
	return true;
}

bool bigNum::Write(char* outFileName)
{
	return fileWrite(bigNum::bigNumArr, bigNum::bigNumSign, bigNum::bigNumArrSize, outFileName, bigNum::base);
}

int* bigNum::fileRead(char* fileIn, int base, int& arrSize, char& numberSign)
{
	int* bigNumArr = NULL;
	const char* flag;
	if (base == 1000000000)
	{
		flag = "r";
	}
	else if (base == 256)
	{
		flag = "rb";
	}

	FILE* fp = fopen(fileIn, flag);
	if (!fp)
	{
		printf("Can't open the file with a big number. Error!\n");
		return bigNumArr;
	}

	fseek(fp, 0, SEEK_END);
	int fileSize = ftell(fp);
	int curPos = 0;

	fseek(fp, 0, SEEK_SET);
	if (fgetc(fp) == '-')
	{
		numberSign = '-';
		curPos = fileSize;
		fileSize -= 1;
	}
	else
	{
		numberSign = '+';
		curPos = fileSize;
	}

	if (base == 1000000000)
	{
		if (!(fileSize % 9))
		{
			arrSize = fileSize / 9;
		}
		else
		{
			arrSize = fileSize / 9 + 1;
		}
	}
	else if (base == 256)
	{
		arrSize = fileSize;
	}

	bigNumArr = new int[arrSize];
	for (int i = 0; i < arrSize; i++)
	{
		bigNumArr[i] = 0;
	}

	if (base == 1000000000)
	{

		for (int i = arrSize; i > 0; i--)
		{
			if ((curPos - 9) >= 0)
			{
				curPos -= 9;
				fseek(fp, curPos, SEEK_SET);
				for (int j = 0; j < 9; j++)
				{
					bigNumArr[i - 1] += (fgetc(fp) - 48)*(int)(pow((double)10, (9 - j - 1)));
				}
			}
			else
			{
				fseek(fp, 0, SEEK_SET);
				if (fgetc(fp) == '-')
				{
					fseek(fp, 1, SEEK_SET);
					for (int j = 1; j < curPos; j++)
					{
						bigNumArr[i - 1] += (fgetc(fp) - 48)*(int)(pow((double)10, (curPos - j - 1)));
					}
				}
				else
				{
					fseek(fp, 0, SEEK_SET);
					for (int j = 0; j < curPos; j++)
					{
						bigNumArr[i - 1] += (fgetc(fp) - 48)*(int)(pow((double)10, (curPos - j - 1)));
					}
				}
			}
		}
	}
	else if (base == 256)
	{
		fseek(fp, 0, SEEK_SET);
		for (int i = arrSize; i > 0; i--)
		{
			bigNumArr[i - 1] = getc(fp);
		}
	}

	fclose(fp);
	printf("The big number is successfully read from file.\n");
	return bigNumArr;
}

bool bigNum::fileWrite(int* bigNumArr, char numSign, int bigNumArrSize, char* fileResultName, int base)
{
	const char* flag = NULL;
	if (base == 1000000000)
	{
		flag = "w";
	}
	else if (base == 256)
	{
		flag = "wb+";
	}

	FILE* fp = fopen(fileResultName, flag);

	if (!fp)
	{
		printf("Can't open the file to write the result! Error!\n");
		return false;
	}

	if (base == 1000000000)
	{
		if (numSign == '-')
		{
			fprintf(fp, "%c", numSign);
		}
		for (int i = 0; i < bigNumArrSize; i++)
		{
			if (i)
			{
				for (int j = 0; j < 9; j++)
				{
					if (bigNumArr[i] < (int)pow((double)10, j))
					{
						fprintf(fp, "%d", 0);
					}
				}
			}
			fprintf(fp, "%d", bigNumArr[i]);
		}
	}

	else if (base == 256)
	{
		for (int i = bigNumArrSize; i > 0; i--)
		{
			putc(bigNumArr[i - 1], fp);
		}
	}

	fclose(fp);
	printf("The big number is successfully written to file.\n");
	return true;
}

char bigNum::resultSign(char operation, char firstNumSign, char secNumSign, int* firstNumArr, int* secNumArr, int firstNumArrSize, int secNumArrSize)
{
	if (operation == '+')
	{
		if (firstNumArrSize > secNumArrSize)
		{
			return firstNumSign;
		}
		else if (firstNumArrSize < secNumArrSize)
		{
			return secNumSign;
		}

		else
		{
			for (int i = 0; i < firstNumArrSize; i++)
			{
				if (firstNumArr[i] > secNumArr[i])
				{
					return firstNumSign;
				}

				else if (firstNumArr[i] < secNumArr[i])
				{
					return secNumSign;
				}
			}
		}

		return '=';
	}

	if (operation == '*' || operation == '/')
	{
		if (firstNumSign != secNumSign)
		{
			return '-';
		}
		else
		{
			return '+';
		}
	}

	return firstNumSign;
}

void bigNum::findMaxMin(int* firstNumArr, int* secNumArr, int firstNumArrSize, int secNumArrSize, int** maxNumArr, int** minNumArr, int& maxNumArrSize, int& minNumArrSize)
{
	if (firstNumArrSize > secNumArrSize)
	{
		maxNumArrSize = firstNumArrSize;
		*maxNumArr = new int[maxNumArrSize];
		for (int i = 0; i < maxNumArrSize; i++)
		{
			(*maxNumArr)[i] = firstNumArr[i];
		}
		minNumArrSize = secNumArrSize;
		*minNumArr = new int[minNumArrSize];
		for (int i = 0; i < minNumArrSize; i++)
		{
			(*minNumArr)[i] = secNumArr[i];
		}
	}

	else if (firstNumArrSize < secNumArrSize)
	{
		maxNumArrSize = secNumArrSize;
		*maxNumArr = new int[maxNumArrSize];
		for (int i = 0; i < maxNumArrSize; i++)
		{
			(*maxNumArr)[i] = secNumArr[i];
		}
		minNumArrSize = firstNumArrSize;
		(*minNumArr) = new int[minNumArrSize];
		for (int i = 0; i < minNumArrSize; i++)
		{
			(*minNumArr)[i] = firstNumArr[i];
		}
	}

	else
	{
		for (int i = 0; i < firstNumArrSize; i++)
		{
			if (firstNumArr[i] > secNumArr[i])
			{
				maxNumArrSize = firstNumArrSize;
				*maxNumArr = new int[maxNumArrSize];
				for (int i = 0; i < maxNumArrSize; i++)
				{
					(*maxNumArr)[i] = firstNumArr[i];
				}
				minNumArrSize = secNumArrSize;
				*minNumArr = new int[minNumArrSize];
				for (int i = 0; i < minNumArrSize; i++)
				{
					(*minNumArr)[i] = secNumArr[i];
				}
				break;
			}

			else if (firstNumArr[i] < secNumArr[i])
			{
				maxNumArrSize = secNumArrSize;
				*maxNumArr = new int[maxNumArrSize];
				for (int i = 0; i < maxNumArrSize; i++)
				{
					(*maxNumArr)[i] = secNumArr[i];
				}
				minNumArrSize = firstNumArrSize;
				*minNumArr = new int[minNumArrSize];
				for (int i = 0; i < minNumArrSize; i++)
				{
					(*minNumArr)[i] = firstNumArr[i];
				}
				break;
			}

			else
			{
				maxNumArrSize = firstNumArrSize;
				*maxNumArr = new int[maxNumArrSize];
				for (int i = 0; i < maxNumArrSize; i++)
				{
					(*maxNumArr)[i] = firstNumArr[i];
				}
				minNumArrSize = secNumArrSize;
				*minNumArr = new int[minNumArrSize];
				for (int i = 0; i < minNumArrSize; i++)
				{
					(*minNumArr)[i] = secNumArr[i];
				}
				break;
			}
		}
	}
}

int* bigNum::withoutNulls(int* arrWithNulls, int& arrSize)
{
	int nullValues = 0;
	int* arrWithoutNulls = NULL;

	for (int i = 0; i < arrSize; i++)
	{
		if (arrWithNulls[i] == 0)
		{
			nullValues++;
		}
		else
		{
			break;
		}
	}

	arrSize -= nullValues;
	if (!arrSize)
	{
		arrSize = 1;
		arrWithoutNulls = new int[arrSize];
		arrWithoutNulls[0] = 0;
	}

	else
	{
		arrWithoutNulls = new int[arrSize];
		for (int i = 0; i < arrSize; i++)
		{
			arrWithoutNulls[i] = arrWithNulls[i + nullValues];
		}
	}

	delete[] arrWithNulls;
	return arrWithoutNulls;
}

int* bigNum::longToInt(long long int ArrElem, int* longToIntArr, int& longToIntArrSize, int base)
{
	longToIntArrSize = 2;
	longToIntArr = new int[longToIntArrSize];
	for (int i = 0; i < longToIntArrSize; i++)
	{
		longToIntArr[i] = 0;
	}

	longToIntArr[0] = (int)(ArrElem / (long long int)base);
	longToIntArr[1] = (int)(ArrElem % (long long int)base);

	return withoutNulls(longToIntArr, longToIntArrSize);
}

int* bigNum::copyArr(int* newArr, int* oldArr, int& newArrSize, int oldArrSize)
{
	newArrSize = oldArrSize;
	newArr = new int[newArrSize];
	for (int i = 0; i < newArrSize; i++)
	{
		newArr[i] = oldArr[i];
	}

	return withoutNulls(newArr, newArrSize);
}

void bigNum::copyBigNum(const bigNum& rhv)
{
	this->base = rhv.base;
	this->bigNumSign = rhv.bigNumSign;
	this->bigNumArr = copyArr(this->bigNumArr, rhv.bigNumArr, this->bigNumArrSize, rhv.bigNumArrSize);
}

bigNum& bigNum::sumOrSub(const bigNum& lhv, const bigNum& rhv, bool isSubmit, char tmpSecSign)
{
	char realOperation = '+';
	bigNum* Result = new bigNum;
	Result->base = lhv.base;

	Result->bigNumSign = resultSign('+', lhv.bigNumSign, tmpSecSign, lhv.bigNumArr, rhv.bigNumArr, lhv.bigNumArrSize, rhv.bigNumArrSize);

	if (lhv.bigNumSign != tmpSecSign)
	{
		realOperation = '-';
	}

	switch (realOperation)
	{
	case '+':
		Result->bigNumArr = addition(lhv.bigNumArr, rhv.bigNumArr, Result->bigNumArr, lhv.bigNumArrSize, rhv.bigNumArrSize, Result->bigNumArrSize, Result->base);
		break;
	case '-':
		Result->bigNumArr = substraction(lhv.bigNumArr, rhv.bigNumArr, Result->bigNumArr, lhv.bigNumArrSize, rhv.bigNumArrSize, Result->bigNumArrSize, Result->base);
		break;
	}

	return *Result;
}

int* bigNum::shiftLeft(int* arrForShift, int& arrSize)
{
	if (!arrSize)
	{
		arrSize = 1;
		arrForShift = new int[arrSize];
		arrForShift[0] = 0;
		return arrForShift;
	}

	int* newArr = new int[arrSize + 1];
	arrSize += 1;
	for (int i = 0; i < arrSize - 1; i++)
	{
		newArr[i] = arrForShift[i];
	}
	newArr[arrSize - 1] = 0;
	delete[] arrForShift;
	return newArr;
}

int* bigNum::addition(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, int base)
{
	int* moreNumArr = NULL;
	int* lessNumArr = NULL;
	int moreNumArrSize = 0;
	int lessNumArrSize = 0;

	findMaxMin(firstNumArr, secondNumArr, firstNumArrSize, secNumArrSize, &moreNumArr, &lessNumArr, moreNumArrSize, lessNumArrSize);
	resNumArrSize = moreNumArrSize + 1;
	resNumArr = new int[resNumArrSize];

	for (int i = 0; i < resNumArrSize; i++)
	{
		resNumArr[i] = 0;
	}

	for (int i = resNumArrSize; i > 1; i--)
	{
		if ((resNumArrSize - i) < lessNumArrSize)
		{
			resNumArr[i - 1] += (moreNumArr[moreNumArrSize - (resNumArrSize - i) - 1] + lessNumArr[lessNumArrSize - (resNumArrSize - i) - 1]);
		}

		else
		{
			resNumArr[i - 1] += moreNumArr[moreNumArrSize - (resNumArrSize - i) - 1];
		}

		resNumArr[i - 2] += resNumArr[i - 1] / base;
		resNumArr[i - 1] %= base;
	}

	delete[] moreNumArr;
	delete[] lessNumArr;
	return withoutNulls(resNumArr, resNumArrSize);
}

int* bigNum::substraction(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, int base)
{
	int* moreNumArr = NULL;
	int* lessNumArr = NULL;
	int moreNumArrSize = 0;
	int lessNumArrSize = 0;
	int credit = 0;
	int newSub = 0;

	findMaxMin(firstNumArr, secondNumArr, firstNumArrSize, secNumArrSize, &moreNumArr, &lessNumArr, moreNumArrSize, lessNumArrSize);
	resNumArrSize = moreNumArrSize;

	resNumArr = new int[resNumArrSize];

	for (int i = 0; i < resNumArrSize; i++)
	{
		resNumArr[i] = 0;
	}

	for (int i = resNumArrSize; i > 0; i--)
	{
		if ((resNumArrSize - i) < lessNumArrSize)
		{
			newSub = moreNumArr[moreNumArrSize - (resNumArrSize - i) - 1] - lessNumArr[lessNumArrSize - (resNumArrSize - i) - 1] - credit;
		}

		else
		{
			newSub = moreNumArr[moreNumArrSize - (resNumArrSize - i) - 1] - credit;
		}

		if (newSub < 0)
		{
			resNumArr[i - 1] = newSub + base;
			credit = 1;
		}
		else
		{
			resNumArr[i - 1] = newSub;
			credit = 0;
		}

	}

	delete[] moreNumArr;
	delete[] lessNumArr;
	return withoutNulls(resNumArr, resNumArrSize);
}

int* bigNum::multiplication(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, int base)
{
	long long int* resNumArrLong = NULL;
	resNumArrSize = firstNumArrSize + secNumArrSize + 1;
	resNumArr = new int[resNumArrSize];
	resNumArrLong = new long long int[resNumArrSize];

	for (int i = 0; i < resNumArrSize; i++)
	{
		resNumArrLong[i] = 0;
		resNumArr[i] = 0;
	}

	for (int i = firstNumArrSize; i > 0; i--)
	{
		for (int j = secNumArrSize; j > 0; j--)
		{
			resNumArrLong[i + j] += (long long int)(firstNumArr[i - 1]) * (long long int)(secondNumArr[j - 1]);
			resNumArrLong[i + j - 1] += resNumArrLong[i + j] / (long long int)base;
			resNumArrLong[i + j] %= (long long int)base;
		}
	}

	for (int i = 0; i < resNumArrSize; i++)
	{
		resNumArr[i] = (int)resNumArrLong[i];
	}

	delete[] resNumArrLong;

	return withoutNulls(resNumArr, resNumArrSize);
}

int* bigNum::divOnDigit(int* firstNumArr, int digit, int* resNumArr, int firstNumArrSize, int& resNumArrSize, int& tail, bool isRem, int base)
{
	if (!digit)
	{
		printf("Dividing to the zero. Error!\n");
		return firstNumArr;
	}

	resNumArrSize = firstNumArrSize;
	resNumArr = new int[resNumArrSize];
	for (int i = 0; i < resNumArrSize; i++)
	{
		resNumArr[i] = 0;
	}

	int remain = 0;
	long long int curDiver = 0;
	for (int i = 0; i < firstNumArrSize; i++)
	{
		curDiver = (long long int)remain * (long long int)base + (long long int)firstNumArr[i];
		resNumArr[i] = (int)(curDiver / (long long int)digit);
		remain = (int)(curDiver % (long long int)digit);
	}

	tail = remain;
	return withoutNulls(resNumArr, resNumArrSize);
}

int* bigNum::dividing(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, bool isRem, int base)
{
	int remain = 0;
	if (secNumArrSize == 1)
	{
		resNumArr = divOnDigit(firstNumArr, secondNumArr[0], resNumArr, firstNumArrSize, resNumArrSize, remain, isRem, base);
		if (isRem)
		{
			delete[] resNumArr;
			resNumArrSize = 1;
			resNumArr = new int[1];
			resNumArr[0] = remain;
			return resNumArr;
		}
		else
		{
			return resNumArr;
		}
	}

	if (firstNumArrSize == 1)
	{
		resNumArrSize = 1;
		resNumArr = new int[resNumArrSize];

		if (secNumArrSize == 1)
		{
			if (secondNumArr[0])
			{
				resNumArr[0] = firstNumArr[0] / secondNumArr[0];
				return resNumArr;
			}
			else
			{
				printf("Dividing to the zero. Error!\n");
				return firstNumArr;
			}
		}
		else
		{
			if (isRem)
			{
				delete[] resNumArr;
				resNumArrSize = 1;
				resNumArr = new int[1];
				resNumArr[0] = firstNumArr[0];
				return resNumArr;
			}
			else
			{
				resNumArr[0] = 0;
				return resNumArr;
			}
		}
	}

	if (firstNumArrSize < secNumArrSize)
	{
		resNumArrSize = 1;
		resNumArr = new int[resNumArrSize];
		resNumArr[0] = 0;
		if (isRem)
		{
			delete[] resNumArr;
			resNumArrSize = firstNumArrSize;
			resNumArr = new int[resNumArrSize];
			for (int i = 0; i < resNumArrSize; i++)
			{
				resNumArr[i] = firstNumArr[i];
			}
			return resNumArr;
		}
		else
		{
			return resNumArr;
		}
	}

	int* curValue = NULL;
	int* cur = NULL;
	int* tempCur = NULL;
	int* middleArr = new int[1];
	middleArr[0] = 0;
	int curValSize = 0;
	int curSize = 0;
	int tempCurSize = 0;

	resNumArrSize = firstNumArrSize;
	resNumArr = new int[resNumArrSize];
	for (int i = 0; i < resNumArrSize; i++)
	{
		resNumArr[i] = 0;
	}

	for (int i = (firstNumArrSize - 1); i >= 0; i--)
	{
		curValue = shiftLeft(curValue, curValSize);
		curValue[curValSize - 1] = firstNumArr[firstNumArrSize - i - 1];

		int curQuot = 0;
		int leftEdge = 0;
		int middle = 0;
		int rightEdge = base;

		while (leftEdge <= rightEdge)
		{
			middle = (leftEdge + rightEdge) / 2;
			middleArr[0] = middle;
			cur = multiplication(secondNumArr, middleArr, cur, secNumArrSize, 1, curSize, base);
			if (resultSign('+', '+', '-', cur, curValue, curSize, curValSize) != '+')
			{
				curQuot = middle;
				leftEdge = middle + 1;
			}
			else
			{
				rightEdge = middle - 1;
			}
			delete[] cur;
		}
		resNumArr[i] = curQuot;
		middleArr[0] = curQuot;
		cur = multiplication(secondNumArr, middleArr, cur, secNumArrSize, 1, curSize, base);

		tempCur = substraction(curValue, cur, tempCur, curValSize, curSize, tempCurSize, base);
		delete[] curValue;
		delete[] cur;
		curValue = copyArr(curValue, tempCur, curValSize, tempCurSize);
		delete[] tempCur;
	}
	
	delete[] middleArr;

	if (isRem)
	{
		delete[] resNumArr;
		resNumArr = withoutNulls(curValue, curValSize);
		resNumArrSize = curValSize;
		return resNumArr;
	}
	else
	{
		delete[] curValue;
		return withoutNulls(resNumArr, resNumArrSize);
	}

}

int* bigNum::dividing2(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, bool isRem, int base)
{
	int remain = 0;
	if (secNumArrSize == 1)
	{
		resNumArr = divOnDigit(firstNumArr, secondNumArr[0], resNumArr, firstNumArrSize, resNumArrSize, remain, isRem, base);
		if (isRem)
		{
			delete[] resNumArr;
			resNumArrSize = 1;
			resNumArr = new int[1];
			resNumArr[0] = remain;
			return resNumArr;
		}
		else
		{
			return resNumArr;
		}
	}

	if (firstNumArrSize == 1)
	{
		resNumArrSize = 1;
		resNumArr = new int[resNumArrSize];

		if (secNumArrSize == 1)
		{
			if (secondNumArr[0])
			{
				resNumArr[0] = firstNumArr[0] / secondNumArr[0];
				return resNumArr;
			}
			else
			{
				printf("Dividing to the zero. Error!\n");
				return firstNumArr;
			}
		}
		else
		{
			if (isRem)
			{
				delete[] resNumArr;
				resNumArrSize = 1;
				resNumArr = new int[1];
				resNumArr[0] = firstNumArr[0];
				return resNumArr;
			}
			else
			{
				resNumArr[0] = 0;
				return resNumArr;
			}
		}
	}
	
	if (firstNumArrSize < secNumArrSize)
	{
		resNumArrSize = 1;
		resNumArr = new int[resNumArrSize];
		resNumArr[0] = 0;
		if (isRem)
		{
			delete[] resNumArr;
			resNumArrSize = firstNumArrSize;
			resNumArr = new int[resNumArrSize];
			for (int i = 0; i < resNumArrSize; i++)
			{
				resNumArr[i] = firstNumArr[i];
			}
			return resNumArr;
		}
		else
		{
			return resNumArr;
		}
	}

	resNumArrSize = firstNumArrSize - secNumArrSize + 1;
	resNumArr = new int[resNumArrSize];
	for (int i = 0; i < resNumArrSize; i++)
	{
		resNumArr[i] = 0;
	}

	int* remainder = NULL;
	int* deduction = NULL;
	int* submit = NULL;
	int* difference = NULL;
	long long int* modifyRem = NULL;
	long long int* modifySecNumArr = NULL;
	int remainderSize = 0;
	int deductionSize = 0;
	int difSize = 0;
	remainderSize = firstNumArrSize + 1;
	remainder = new int[remainderSize];
	submit = new int[remainderSize];
	modifyRem = new long long int[remainderSize];
	modifySecNumArr = new long long int[secNumArrSize];
	for (int i = 0; i < remainderSize; i++)
	{
		remainder[i] = 0;
		modifyRem[i] = 0;
		submit[i] = 0;
	}

	for (int i = 0; i < secNumArrSize; i++)
	{
		modifySecNumArr[i] = 0;
	}

	int helpValue = 0;
	if (!((base / 2) % secondNumArr[0]))
	{
		helpValue = ((base / 2) / secondNumArr[0]);
	}

	else
	{
		helpValue = ((base / 2) / secondNumArr[0]) + 1;
	}

	for (int i = 1; i < remainderSize; i++)
	{
		remainder[i] = firstNumArr[i - 1];
	}

	for (int i = 0; i < secNumArrSize; i++)
	{
		modifySecNumArr[i] = (long long int)secondNumArr[i] * (long long int)helpValue;
	}

	int* newQuot = NULL;
	newQuot = new int[1];
	int* modifyRemInt = NULL;
	int* modifySecNumArrInt = NULL;
	int* multiArr = NULL;
	int* secMultiArr = NULL;
	int* thirMultiArr = NULL;
	int* sumArr = NULL;
	int* baseArr = NULL;
	int* relation = NULL;
	baseArr = new int[1];
	baseArr[0] = base;
	int multiArrSize = 0;
	int secMultiArrSize = 0;
	int thirMultiArrSize = 0;
	int sumArrSize = 0;
	int modifyRemIntSize = 0;
	int modifySecNumArrIntSize = 0;
	int relationSize = 0;

	for (int i = 0; i < resNumArrSize; i++)
	{
		for (int j = 0; j < remainderSize; j++)
		{
			modifyRem[j] = (long long int)remainder[j] * (long long int)helpValue;
		}

		modifyRemInt = longToInt(modifyRem[i], modifyRemInt, modifyRemIntSize, base);
		multiArr = multiplication(modifyRemInt, baseArr, multiArr, modifyRemIntSize, 1, multiArrSize, base);
		delete[] modifyRemInt;
		modifyRemInt = longToInt(modifyRem[i + 1], modifyRemInt, modifyRemIntSize, base);
		sumArr = addition(multiArr, modifyRemInt, sumArr, multiArrSize, modifyRemIntSize, sumArrSize, base);
		delete[] modifyRemInt;
		relation = divOnDigit(sumArr, (int)modifySecNumArr[0], relation, sumArrSize, relationSize, remain, false, base);

		if (relationSize > 1)
		{
			newQuot[0] = (base - 1);
		}
		else
		{
			newQuot[0] = relation[0];
		}

		delete[] relation;

		do
		{
			delete[] multiArr;
			delete[] sumArr;

			modifySecNumArrInt = longToInt(modifySecNumArr[1], modifySecNumArrInt, modifySecNumArrIntSize, base);
			multiArr = multiplication(modifySecNumArrInt, newQuot, multiArr, modifySecNumArrIntSize, 1, multiArrSize, base);
			delete[] modifySecNumArrInt;

			modifyRemInt = longToInt(modifyRem[i], modifyRemInt, modifyRemIntSize, base);
			secMultiArr = multiplication(modifyRemInt, baseArr, secMultiArr, modifyRemIntSize, 1, secMultiArrSize, base);
			delete[] modifyRemInt;
			modifyRemInt = longToInt(modifyRem[i + 1], modifyRemInt, modifyRemIntSize, base);
			sumArr = addition(secMultiArr, modifyRemInt, sumArr, secMultiArrSize, modifyRemIntSize, sumArrSize, base);
			delete[] modifyRemInt;
			delete[] secMultiArr;
			modifySecNumArrInt = longToInt(modifySecNumArr[0], modifySecNumArrInt, modifySecNumArrIntSize, base);
			secMultiArr = multiplication(modifySecNumArrInt, newQuot, secMultiArr, modifySecNumArrIntSize, 1, secMultiArrSize, base);
			delete[] modifySecNumArrInt;
			thirMultiArr = substraction(sumArr, secMultiArr, thirMultiArr, sumArrSize, secMultiArrSize, thirMultiArrSize, base);
			delete[] sumArr;
			delete[] secMultiArr;
			secMultiArr = multiplication(thirMultiArr, baseArr, secMultiArr, thirMultiArrSize, 1, secMultiArrSize, base);
			delete[] thirMultiArr;
			modifyRemInt = longToInt(modifyRem[i + 2], modifyRemInt, modifyRemIntSize, base);
			sumArr = addition(secMultiArr, modifyRemInt, sumArr, secMultiArrSize, modifyRemIntSize, sumArrSize, base);
			delete[] secMultiArr;
			delete[] modifyRemInt;

			if (resultSign('+', '+', '-', multiArr, sumArr, multiArrSize, sumArrSize) == '+')
			{
				newQuot[0]--;
			}
		} while (resultSign('+', '+', '-', multiArr, sumArr, multiArrSize, sumArrSize) == '+');

		delete[] multiArr;
		delete[] sumArr;
		deduction = multiplication(secondNumArr, newQuot, deduction, secNumArrSize, 1, deductionSize, base);
		for (int j = 0; j < (i + 1 - (deductionSize - secNumArrSize)); j++)
		{
			submit[j] = 0;
		}
		for (int j = (i + 1 - (deductionSize - secNumArrSize)); j < (secNumArrSize + 1 + i); j++)
		{
			submit[j] = deduction[j - i - 1 + (deductionSize - secNumArrSize)];
		}
		for (int j = (secNumArrSize + 1 + i); j < remainderSize; j++)
		{
			submit[j] = 0;
		}

		if (resultSign('+', '+', '-', remainder, submit, remainderSize, remainderSize) == '-')
		{
			newQuot[0]--;

			delete[] deduction;

			deduction = multiplication(secondNumArr, newQuot, deduction, secNumArrSize, 1, deductionSize, base);
			for (int j = 0; j < (i + 1 - (deductionSize - secNumArrSize)); j++)
			{
				submit[j] = 0;
			}
			for (int j = (i + 1 - (deductionSize - secNumArrSize)); j < (secNumArrSize + 1 + i); j++)
			{
				submit[j] = deduction[j - i - 1 + (deductionSize - secNumArrSize)];
			}
			for (int j = (secNumArrSize + 1 + i); j < remainderSize; j++)
			{
				submit[j] = 0;
			}
		}

		difference = substraction(remainder, submit, difference, remainderSize, remainderSize, difSize, base);
		resNumArr[i] = newQuot[0];
		for (int i = remainderSize; i >(remainderSize - difSize); i--)
		{
			remainder[i - 1] = difference[difSize - (remainderSize - i) - 1];
		}
		for (int i = (remainderSize - difSize); i > 0; i--)
		{
			remainder[i - 1] = 0;
		}
		delete[] difference;
		delete[] deduction;
	}

	delete[] submit;
	delete[] modifyRem;
	delete[] modifySecNumArr;
	delete[] newQuot;
	delete[] baseArr;

	if (isRem)
	{
		delete[] resNumArr;
		resNumArr = withoutNulls(remainder, remainderSize);
		resNumArrSize = remainderSize;
		return resNumArr;
	}
	else
	{
		delete[] remainder;
		return withoutNulls(resNumArr, resNumArrSize);
	}
}

int* bigNum::involution(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, int base)
{
	resNumArr = new int[1];
	resNumArr[0] = 1;
	resNumArrSize = 1;
	int* oneArr = NULL;
	oneArr = new int[1];
	oneArr[0] = 1;
	int* tempQuotArr = NULL;
	int tempQuotArrSize = 0;
	int* tempMultiArr = NULL;
	int tempMultiArrSize = 0;
	int* tempSubArr = NULL;
	int tempSubArrSize = 0;
	int* tempFirstArr = NULL;
	int tempFirstArrSize = 0;
	int* tempSecArr = NULL;
	int tempSecArrSize = 0;
	int remain = 0;

	tempFirstArrSize = firstNumArrSize;
	tempFirstArr = new int[tempFirstArrSize];
	for (int i = 0; i < tempFirstArrSize; i++)
	{
		tempFirstArr[i] = firstNumArr[i];
	}
	tempSecArrSize = secNumArrSize;
	tempSecArr = new int[tempSecArrSize];
	for (int i = 0; i < tempSecArrSize; i++)
	{
		tempSecArr[i] = secondNumArr[i];
	}

	while (!((tempSecArrSize == 1) && (tempSecArr[0] == 0)))
	{
		tempQuotArr = divOnDigit(tempSecArr, 2, tempQuotArr, tempSecArrSize, tempQuotArrSize, remain, false, base);
		if (!remain)
		{
			tempSecArr = copyArr(tempSecArr, tempQuotArr, tempSecArrSize, tempQuotArrSize);
			tempMultiArr = multiplication(tempFirstArr, tempFirstArr, tempMultiArr, tempFirstArrSize, tempFirstArrSize, tempMultiArrSize, base);
			tempFirstArr = copyArr(tempFirstArr, tempMultiArr, tempFirstArrSize, tempMultiArrSize);
		}
		else
		{
			tempSubArr = substraction(tempSecArr, oneArr, tempSubArr, tempSecArrSize, 1, tempSubArrSize, base);
			tempSecArr = copyArr(tempSecArr, tempSubArr, tempSecArrSize, tempSubArrSize);
			tempMultiArr = multiplication(tempFirstArr, resNumArr, tempMultiArr, tempFirstArrSize, resNumArrSize, tempMultiArrSize, base);
			resNumArr = copyArr(resNumArr, tempMultiArr, resNumArrSize, tempMultiArrSize);
		}
	}

	//tempMultiArr = multiplication(tempFirstArr, resNumArr, tempMultiArr, tempFirstArrSize, resNumArrSize, tempMultiArrSize, base);
	//resNumArr = copyArr(resNumArr, tempMultiArr, resNumArrSize, tempMultiArrSize);

	delete[] oneArr;
	delete[] tempSecArr;
	delete[] tempFirstArr;

	return resNumArr;
}

int* bigNum::remainder(int* firstNumArr, int* secondNumArr, int* resNumArr, int firstNumArrSize, int secNumArrSize, int& resNumArrSize, int base)
{
	resNumArr = dividing(firstNumArr, secondNumArr, resNumArr, firstNumArrSize, secNumArrSize, resNumArrSize, true, base);
	return resNumArr;
}