#include <bits/stdc++.h>

#define ll long long

using namespace std;

void solution() {
    ll t,q,d;
    cin>>t>>q>>d;
    while(t--) {
        ll smallX=1e18;
        smallX*=-1;
        smallX--;
        ll bigX=1e18;
        bigX++;
        ll smallY=smallX;
        ll bigY=bigX;
        ll cpower=1;
        string ans;
        while(true) {
            if(cpower==1) {
                if(bigX>=(smallX+2) && bigY>=(smallY+2)) {
                    ll midX=(bigX+smallX)/2;
                    ll midY=(bigY+smallY)/2;
                    cout<<cpower<<" "<<midX<<" "<<midY<<endl;
                    cin>>ans;
                    if(ans=="O" || ans=="FAILED") {
                        break;
                    }
                    if(ans[0]=='X') {
                        smallX=midX-1;
                        bigX=midX+1;
                    }
                    else if(ans[0]=='P') {
                        if(d==0) {
                            bigX=midX-1;
                        }
                        else {
                            bigX=midX;
                            smallX--;
                        }
                    }
                    else {
                        if(d==0) {
                            smallX=midX+1;
                        }
                        else {
                            smallX=midX;
                            bigX++;
                        }
                    }
                    if(ans[1]=='Y') {
                        smallY=midY-1;
                        bigY=midY+1;
                    }
                    else if(ans[1]=='P') {
                        if(d==0) {
                            bigY=midY-1;
                        }
                        else {
                            bigY=midY;
                            smallY--;
                        }
                    }
                    else {
                        if(d==0) {
                            smallY=midY+1;
                        }
                        else {
                            smallY=midY;
                            bigY++;
                        }
                    }
                    if(d!=0) {
                        if(bigX<=(smallX+3) && bigY<=(smallY+3)) {
                            cpower=2;
                        }
                    } 
                }
                else {
                    cpower=2;
                    cout<<cpower<<" "<<smallX<<" "<<smallY<<" "<<bigX<<" "<<bigY<<endl;
                    cin>>ans;
                    break;
                }
            }
            else {
                if(bigX==(smallX+3) && bigY==(smallY+3)) {
                    cout<<cpower<<" "<<smallX<<" "<<smallY<<" "<<smallX+2<<" "<<bigY<<endl;
                    cin>>ans;
                    if(ans=="O") {
                        break;
                    }
                    else if(ans=="IN") {
                        bigX=smallX+2;
                    }
                    else if(ans=="OUT") {
                        smallX=smallX+2;
                        bigX++;
                    }
                }
                if(bigX==smallX+2 && bigY==smallY+3) {
                cout<<cpower<<" "<<smallX<<" "<<smallY<<" "<<bigX<<" "<<smallY+2<<endl;
                cin>>ans;
                if(ans=="IN") {
                    cout<<cpower<<" "<<smallX<<" "<<smallY<<" "<<bigX<<" "<<smallY+2<<endl;
                    cin>>ans;
                }
                else if(ans=="OUT") {
                    cout<<cpower<<" "<<smallX<<" "<<smallY+2<<" "<<bigX<<" "<<smallY+4<<endl;
                    cin>>ans;
                }
                break;
            }
            if(bigX==smallX+3 && bigY==smallY+2) {
                cout<<cpower<<" "<<smallX<<" "<<smallY<<" "<<smallX+2<<" "<<bigY<<endl;
                cin>>ans;
                if(ans=="IN") {
                    cout<<cpower<<" "<<smallX<<" "<<smallY<<" "<<smallX+2<<" "<<bigY<<endl;
                    cin>>ans;
            }
            else if(ans=="OUT") {
                cout<<cpower<<" "<<smallX+2<<" "<<smallY<<" "<<smallX+4<<" "<<bigY<<endl;
                cin>>ans;
            }
            break;
        }
        else {
            cout<<cpower<<" "<<smallX<<" "<<smallY<<" "<<bigX<<" "<<bigY<<endl;
            cin>>ans;
            break;
        }
            }
            
        }
        
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    solution();
	return 0;
}
