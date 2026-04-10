#include<bits/stdc++.h>
using namespace std;
int n, k, ct;
bool vis[10]; 
char mp[10][10]; 
void dfs(int l, int m)
{
    if(m == 0) 
    { 
        ct++;
        return;
    }
    if(n-l+1 < m) 
        return;
    dfs(l+1, m);
    for(int i = 1; i <= n; ++i) 
    {
        if(vis[i] == false && mp[l][i] == '#') 
        {
            vis[i] = true;
            dfs(l+1, m-1); 
            vis[i] = false;
        }
    }
}
int main()
{
    while(cin >> n >> k)
    {
        if(n == -1 && k == -1)
            break;
        memset(vis, 0, sizeof(vis));
        ct = 0;
        for(int i = 1; i <= n; ++i) 
            for(int j = 1; j <= n; ++j)
                cin >> mp[i][j];
        dfs(1, k);
        cout << ct << endl; 
    }
    return 0;
}