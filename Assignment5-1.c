#include <stdio.h>

void growing(int,int);
void shrinking(int,int);

int main()
{
	int x = 3;

	growing(x,0);
	shrinking(0,2*x-2);

	return 0;
}

void growing(int n, int space){
	
	if(n<=0)
		return;
	int i=0;
	for(i=0;i<n-1;i++)
		printf(" ");
	printf("/");
	
	for(i=0;i<space;i++)
		printf(" ");
	printf("\\\n");
	
	growing(n-1, space+2);
	
}

void shrinking(int n, int space){
		
	if(space<0)
		return;
	int i=0;
	for(i=0;i<n;i++)
		printf(" ");
	printf("\\");
	
	for(i=0;i<space;i++)
		printf(" ");
	printf("/\n");
	
	shrinking(n+1, space-2);
	
}

