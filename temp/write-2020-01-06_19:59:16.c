#include <stdio.h>


int add(int a ,int b , int c){
	return c + b;
}

int sub( int a, int b){
	return a - b;
}

int wrapper( int a , int b , int (*func)(int , int) ){
	return func(a,b);
} 

int main(){
	
	int (*a)(int , int) = add;
	int (*s)(int , int) = sub;

	enum shape  { circle , square } ;
	enum colour { red , blue };
	enum colour bgd;
	int c = blue;
	{
		int m = 10;
		printf("%d"

	}
	
	 
	
	
}
