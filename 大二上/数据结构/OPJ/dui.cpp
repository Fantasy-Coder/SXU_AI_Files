#include <iostream>
#include <memory.h>
#include <vector>
#include <queue>
#include <stdio.h>
#include <algorithm>
#include <unordered_set>
#include <set>
#include <math.h>
#include <functional>
#define IN (1<<28)
using namespace std;
priority_queue<int, vector<int>, greater<int> > q;
int T, N;
int main()
{
    scanf("%d", &T);
    while( T-- )
    {
        scanf("%d", &N);
        while( !q.empty() )
            q.pop();
        while( N-- )
        {
            int Type;
            scanf("%d", &Type);
            if( Type == 1 )
            {
                int value;
                scanf("%d", &value);
                q.push( value );
            }
            else
            {
                int res = q.top();
                q.pop();
                printf("%d\n", res);
            }
        }
    }
 
    return 0;
}