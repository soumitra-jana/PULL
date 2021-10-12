/*
 * author: aman sonkar
 */
#include<bits/stdc++.h>
#define fastIO ios_base::sync_with_stdio(false);cin.tie(NULL);cout.tie(NULL)
using namespace std;
#define MAX 515

int N,M;
int C[MAX], D[MAX][MAX];
vector<pair<int,int>> sortedC;
stack<pair<int,int>> stck[MAX];
vector<int> QueryType,A;
vector<pair<int,int>> QueryData;
int mp[MAX],revmp[MAX],remsz[MAX];
stack<int> vacancy;

void fun1(int i){
    if(stck[i].empty()){
        vacancy.push(i);
        return;
    }
    pair<int,int> pr=stck[i].top();
    if(stck[i].size()==1&&mp[pr.first]==0){
        mp[pr.first]=i;
        revmp[i]=pr.first;
        return;
    }
    if(mp[pr.first]!=0){
        if(mp[pr.first]==i) return;
        for(int j=0;j<pr.second;j++){
            QueryType.push_back(1);
            QueryData.push_back({i,mp[pr.first]});
        }
        if(stck[mp[pr.first]].empty()) stck[mp[pr.first]].push(pr);
        else stck[mp[pr.first]].top().second+=pr.second;
        stck[i].pop();
        remsz[i]+=pr.second;
        remsz[mp[pr.first]]-=pr.second;
        fun1(i);
    }else if(!vacancy.empty()){
        mp[pr.first]=vacancy.top();
        revmp[vacancy.top()]=pr.first;
        vacancy.pop();
        fun1(i);
    }
    return;
}

bool untilTrue=true;
void fun2(){
    for(int i=sortedC.size()-1;i>=0;i--){
        int idx=sortedC[i].second;
        while(true){
            fun1(idx);
            if(stck[idx].empty()||(mp[stck[idx].top().first]==idx)) break;
            pair<int,int> pr=stck[idx].top();
            vector<pair<int,int>> ttV;
            for(int j=0;j<sortedC.size();j++){
                int idx1=sortedC[j].second;
                if(idx==idx1) break;
                if(stck[idx1].empty()) ttV.push_back({0,idx1});
                else if(D[pr.first][stck[idx1].top().first]!=-1){
                    int cost=D[pr.first][stck[idx1].top().first];
                    if(remsz[idx1]<pr.second) cost+=(pr.second-remsz[idx1])*C[idx1];
                    ttV.push_back({cost,idx1});
                }
            }
            if(ttV.empty()) break;
            sort(ttV.begin(),ttV.end());
            int idx1=ttV[0].second;
            if(stck[idx1].empty()||(D[pr.first][stck[idx1].top().first]!=-1)){
                mp[revmp[idx1]]=0;
                for(int k=0;k<pr.second;k++){
                    if(remsz[idx1]==0){
                        QueryType.push_back(2);
                        QueryData.push_back({idx1,idx1});
                        remsz[idx1]++;
                    }
                    QueryType.push_back(1);
                    QueryData.push_back({idx,idx1});
                    remsz[idx1]--;
                }
                if(!stck[idx1].empty()&&stck[idx1].top().first==pr.first) stck[idx1].top().second+=pr.second;
                else stck[idx1].push(pr);
                stck[idx].pop();
                remsz[idx]+=pr.second;
            }
        }
        if(stck[idx].size()>1) untilTrue=true;
    }
    return;
}

int main(){
	//fastIO;
	cin>>N>>M; 
    for(int i=1;i<=N+2;i++){
        cin>>C[i];
        sortedC.push_back({C[i],i});
    }
    sort(sortedC.begin(),sortedC.end());
    for(int i=1;i<=N;i++){
        for(int j=1;j<=N;j++) cin>>D[i][j];
    }
    int B[N+1][M+1];
    for(int i=1;i<=N;i++){
        for(int j=1;j<=M;j++){
            cin>>B[i][j];
            if(!stck[i].empty()&&stck[i].top().first==B[i][j]) stck[i].top().second++;
            else stck[i].push({B[i][j],1});
        }
        if((i==sortedC[0].second||i==sortedC[1].second)&&B[i][1]<B[i][M]){
            stack<pair<int,int>> tstck;
            while(!stck[i].empty()){
                tstck.push(stck[i].top());
                stck[i].pop();
            }
            stck[i]=tstck;
            A.push_back(i);
        }
    }
    remsz[N+1]=remsz[N+2]=M;
    while(untilTrue){
        untilTrue=false;
        fun2();
    }
    
    // for(int i=1;i<=N+2;i++){
    //     cout<<"size : "<<stck[i].size()<<" , contents : \n";
    //     while(!stck[i].empty()){
    //         cout<<stck[i].top().first<<" "<<stck[i].top().second<<"\n";
    //         stck[i].pop();
    //     }
    // }

    // Output :
    cout<<A.size()<<" "<<QueryType.size()<<"\n";
    for(int ele:A) cout<<ele<<" ";
    cout<<"\n";
    for(int i=0;i<QueryType.size();i++){
        if(QueryType[i]==1) cout<<1<<" "<<QueryData[i].first<<" "<<QueryData[i].second<<"\n";
        else if(QueryType[i]==2) cout<<2<<" "<<QueryData[i].first<<"\n";
    }
	return 0;
}
