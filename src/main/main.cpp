#include <bits/stdc++.h>
using namespace std;

string in;
string name;

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout << "\033[32mMFT shell v1.0 (C)\033[0m\n";
    cout << "\033[32mType 'help' for help, type 'exit' to exit. Please create a mod first!\n\033[0m";
    cout << "notice:\n";
    cout << "1. Icon do not add '.png'\n";
    cout << "2. Put the texture file in the appropriate subfolders inside 'textures/*'\n\n";
    
    while(true){
        cout << "\033[34mMFT> \033[0m";
        cin >> in;
        
        if(in == "help" || in == "h" || in == "?" || in == "H" || in == "Help" || in == "HELP"){
            cout << "fd-mod {name:\" \",des:\" \"}  --- to create a mod\n";
            cout << "fd-block {name:\" \",des:\" \",icon:\" \"}  --- to create a block. Icon do not add '.png'\n";
        }
        else if(in == "exit" || in == "quit" || in == "EXIT" || in == "QUIT"){
            break;
        }
        else if(in == "fd-mod"){
            // 使用popen获取Python脚本输出
            string cmd = "python3 ../src/py/fd-mod.py " + in;
            FILE* pipe = popen((cmd + " \"" + in + "\"").c_str(), "r");
            if(pipe){
                char buffer[4096];
                string result = "";
                while(fgets(buffer, sizeof(buffer), pipe) != NULL){
                    result += buffer;
                }
                pclose(pipe);
                
                // 解析返回的mod名称
                size_t pos = result.find("name:");
                if(pos != string::npos){
                    name = result.substr(pos + 5);
                    // 去除换行符和空格
                    name.erase(remove_if(name.begin(), name.end(), ::isspace), name.end());
                }
                cout << "Mod created successfully!\n";
            }
        }
        else if(in == "fd-block"){
            if(name.empty()){
                cout << "Error: Please create a mod first using 'fd-mod' command!\n";
                continue;
            }
            // 使用popen获取Python脚本输出
            string cmd = "python3 ../src/py/fd-block.py " + in;
            FILE* pipe = popen((cmd + " \"" + in + ";name=" + name + ";\"").c_str(), "r");
            if(pipe){
                char buffer[4096];
                string result = "";
                while(fgets(buffer, sizeof(buffer), pipe) != NULL){
                    result += buffer;
                }
                pclose(pipe);
                cout << "Block created successfully!\n";
            }
        }
        else{
            cout << "Unknown command: " << in << "\n";
            cout << "Type 'help' for available commands.\n";
        }
    }
    return 0;
}

