#include<bits/stdc++.h>
using namespace std;

string in;
string name;

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout<<"\033[32mMTF shell v1.0 (C)\033[0m\n";
    cout<<"\033[32mType 'help' for help , type 'exit' to exit.Pleas found a mod first!\n\n\033[0m";
    while(true){
        cout<<"\033[34mMTF> \033[0m";
        cin>>in;
        if(in=="help" || in=="h" || in=="?" || in=="H" || in=="Help" || in=="HELP"){
            cout<<"fd-mod {name:\" \",des:\" \"}  --- to found a mod";
            cout<<"fd-mod-block {name:\" \",des:\" \",icon:\" \"}  --- to found a mod block";
        }
        else if(in=="exit" || in=="quit" || in=="EXIT" || in=="QUIT"){
            break;
        }
        else{
            bool found = (in.find("fd-mod") != string::npos); 
            if(found==1){
                system(in.c_str());
                FILE* pipe = popen(in.c_str(), "r");
                char buffer[4096];
                string result = "";
                while (fgets(buffer, sizeof(buffer), pipe) != NULL) {
                    result += buffer;
                }
                pclose(pipe);
                name = result; 
            }
            else{
                system(in.c_str());
            }
        }
    }
}