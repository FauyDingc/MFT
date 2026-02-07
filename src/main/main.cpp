#include <bits/stdc++.h>
using namespace std;

string get_program_path() {//获取运行目录（写的难受丢给GPT写的）
    char result[PATH_MAX];
    ssize_t count = readlink("/proc/self/exe", result, PATH_MAX);
    string path = (count != -1) ? string(result, count) : "";
    size_t pos = path.find_last_of("/");
    if (pos != string::npos) {
        return path.substr(0, pos);
    }
    return ".";
}

string trim(const string& str) {//去空格，没什么用，以防万一
    size_t start = str.find_first_not_of(" \t\n\r");
    if (start == string::npos) return "";
    size_t end = str.find_last_not_of(" \t\n\r");
    return str.substr(start, end - start + 1);
}

string in;
string name;

int main(){
    
    string program_path = get_program_path();
    
    // --------
    // 尝试多种相对路径找到Python脚本
    string py_path = program_path + "/../script/py/";

    if(access(py_path.c_str(), F_OK) != 0){
        py_path = "./script/py/";
    }
    if(access(py_path.c_str(), F_OK) != 0){
        py_path = "../script/py/";
    }
    if(access(py_path.c_str(), F_OK) != 0){
        py_path = program_path + "/../script/py/";
    }
    if(access(py_path.c_str(), F_OK) != 0){
        cerr << "\033[31mError: Cannot find Python scripts directory!\033[0m\n";
        cerr << "\033[31mSearched paths relative to program and current directory.\033[0m\n";
        return 1;
    }
    // ---------看看py脚本在何处

    cout << "\033[32mMFT shell v1.0 (C)\033[0m\n";
    cout << "\033[32mPython scripts path: " << py_path << "\033[0m\n";
    cout << "\033[32mType 'help' for help, type 'exit' to exit. Please create a mod first!\n\033[0m";
    cout << "notice:\n";
    cout << "   1. Icon do not add '.png'\n";
    cout << "   2. Put the texture file in the appropriate subfolders inside 'textures/*'\n\n";
    
    while(true){
        cout << "\033[34mMFT> \033[0m";
        getline(cin, in);
        
        in = trim(in);
        
        if(in.empty()) continue;
        
        string cmd_name = "";
        string params = "";
        
        //提取参数（单词）
        size_t space_pos = in.find(' ');
        if(space_pos != string::npos){
            cmd_name = in.substr(0, space_pos);
            params = in.substr(space_pos + 1);
        } else {
            cmd_name = in;
        }
        
        // 转换命令名为小写，建议无视他
        string cmd_lower = cmd_name;
        transform(cmd_lower.begin(), cmd_lower.end(), cmd_lower.begin(), ::tolower);
        
        //帮助
        if(cmd_lower == "help" || cmd_lower == "h" || cmd_lower == "?"){
            cout << "\nfd-mod {name:\" \",des:\" \"}  --- to create a mod\n";
            cout << "fd-block {name:\" \",des:\" \",icon:\" \",explosion:\" \",light:\" \"}  --- to create a block\n";
            cout << "fd-item {name:\" \",des:\" \",type:\"2d/3d\",texture:\" \",edible:\"true/false\",effect:\" \",hand:\" \"}  --- to create an item\n";
            cout << "exit/quit  --- to exit the program\n\n";
        }
        else if(cmd_lower == "exit" || cmd_lower == "quit"){
            cout<<'\n';//后面发现直接推出终端不会换行，加了一句
            break;
        }
        else if(cmd_lower == "fd-mod"){
            // 检查参数，看看有没有创建模组，不然会崩
            if(params.empty()){
                cout << "\033[31mError: Please provide parameters. Usage: fd-mod {name:\"mod_name\",des:\"description\"}\033[0m\n";
                continue;
            }
            
            // 传参给Python脚本
            string full_cmd = "python3 -u \"" + py_path + "fd-mod.py\" " + params;
            FILE* pipe = popen(full_cmd.c_str(), "r");
            if(pipe){
                char buffer[4096];
                string result = "";
                while(fgets(buffer, sizeof(buffer), pipe) != NULL){
                    result += buffer;
                }
                pclose(pipe);
                
                // 解析返回的mod名称，新建方块物品要用，放到变量里
                size_t pos = result.find("name:");
                if(pos != string::npos){
                    name = result.substr(pos + 5);
                    // 去除换行符和空格
                    name.erase(remove_if(name.begin(), name.end(), ::isspace), name.end());
                }
                cout << "Mod created successfully!\n";//nice
            } else {
                cout << "\033[31mError: Failed to execute Python script!\033[0m\n";
            }
        }
        else if(cmd_lower == "fd-block"){
            if(name.empty()){
                cout << "\033[31mError: Please create a mod first using 'fd-mod' command!\033[0m\n";
                continue;
            }
            if(params.empty()){
                cout << "\033[31mError: Please provide parameters. Usage: fd-block {name:\"block_name\",des:\"description\",icon:\"texture_name\"}\033[0m\n";
                continue;
            }
            
            // 依旧传参
            string full_cmd = "python3 -u \"" + py_path + "fd-block.py\" " + params + ";name=" + name + ";";
            FILE* pipe = popen(full_cmd.c_str(), "r");
            if(pipe){
                char buffer[4096];
                string result = "";
                while(fgets(buffer, sizeof(buffer), pipe) != NULL){
                    result += buffer;
                }
                pclose(pipe);
                cout << "Block created successfully!\n";
            } else {
                cout << "\033[31mError: Failed to execute Python script!\033[0m\n";
            }
        }
        else if(cmd_lower == "fd-item"){
            if(name.empty()){
                cout << "\033[31mError: Please create a mod first using 'fd-mod' command!\033[0m\n";
                continue;
            }
            if(params.empty()){
                cout << "\033[31mError: Please provide parameters. Usage: fd-item {name:\"item_name\",des:\"description\",type:\"2d/3d\",texture:\"texture_name\"}\033[0m\n";
                continue;
            }
            
            // 传递参数给Python脚本，添加mod名称
            string full_cmd = "python3 -u \"" + py_path + "fd-item.py\" " + params + ";name=" + name + ";";
            FILE* pipe = popen(full_cmd.c_str(), "r");
            if(pipe){
                char buffer[4096];
                string result = "";
                while(fgets(buffer, sizeof(buffer), pipe) != NULL){
                    result += buffer;
                }
                pclose(pipe);
                cout << "Item created successfully!\n";
            } else {
                cout << "\033[31mError: Failed to execute Python script!\033[0m\n";
            }
        }
        else{
            cout << "\033[31mUnknown command: " << cmd_name << "\033[0m\n";
            cout << "\033[31mType 'help' for available commands.\033[0m\n";
        }
    }
    return 0;
}

//作者英文不好，输出的错误信息是先中文再AI帮忙翻译的哈

