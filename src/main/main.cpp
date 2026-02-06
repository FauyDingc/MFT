#include <bits/stdc++.h>
using namespace std;

// 获取程序所在目录的绝对路径
string get_program_path() {
    char result[PATH_MAX];
    ssize_t count = readlink("/proc/self/exe", result, PATH_MAX);
    string path = (count != -1) ? string(result, count) : "";
    // 获取目录部分
    size_t pos = path.find_last_of("/");
    if (pos != string::npos) {
        return path.substr(0, pos);
    }
    return ".";
}

// 去除字符串两端空格
string trim(const string& str) {
    size_t start = str.find_first_not_of(" \t\n\r");
    if (start == string::npos) return "";
    size_t end = str.find_last_not_of(" \t\n\r");
    return str.substr(start, end - start + 1);
}

string in;
string name;

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    
    // 获取程序所在目录
    string program_path = get_program_path();
    
    // 计算Python脚本的绝对路径（无论从哪个目录运行都能找到）
    string py_path = program_path + "/../src/py/";
    
    // 如果在src/main目录下运行，需要使用上级的src目录
    // 检查路径是否存在，如果不存在则尝试其他路径
    if(access(py_path.c_str(), F_OK) != 0){
        // 尝试从项目根目录运行的情况
        py_path = program_path + "/src/py/";
    }
    if(access(py_path.c_str(), F_OK) != 0){
        // 尝试直接使用当前工作目录
        py_path = program_path + "/../../src/py/";
    }
    
    cout << "\033[32mMFT shell v1.0 (C)\033[0m\n";
    cout << "\033[32mPython scripts path: " << py_path << "\033[0m\n";
    cout << "\033[32mType 'help' for help, type 'exit' to exit. Please create a mod first!\n\033[0m";
    cout << "notice:\n";
    cout << "1. Icon do not add '.png'\n";
    cout << "2. Put the texture file in the appropriate subfolders inside 'textures/*'\n\n";
    
    while(true){
        cout << "\033[34mMFT> \033[0m";
        // 使用getline读取完整命令（包括参数）
        getline(cin, in);
        
        // 去除首尾空格
        in = trim(in);
        
        if(in.empty()) continue;
        
        // 解析命令名和参数
        string cmd_name = "";
        string params = "";
        
        // 提取命令名（第一个单词）
        size_t space_pos = in.find(' ');
        if(space_pos != string::npos){
            cmd_name = in.substr(0, space_pos);
            params = in.substr(space_pos + 1);
        } else {
            cmd_name = in;
        }
        
        // 转换命令名为小写进行匹配
        string cmd_lower = cmd_name;
        transform(cmd_lower.begin(), cmd_lower.end(), cmd_lower.begin(), ::tolower);
        
        if(cmd_lower == "help" || cmd_lower == "h" || cmd_lower == "?"){
            cout << "fd-mod {name:\" \",des:\" \"}  --- to create a mod\n";
            cout << "fd-block {name:\" \",des:\" \",icon:\" \",explosion:\" \",light:\" \"}  --- to create a block\n";
            cout << "fd-item {name:\" \",des:\" \",type:\"2d/3d\",texture:\" \",edible:\"true/false\",effect:\" \",hand:\" \"}  --- to create an item\n";
            cout << "exit/quit  --- to exit the program\n";
        }
        else if(cmd_lower == "exit" || cmd_lower == "quit"){
            break;
        }
        else if(cmd_lower == "fd-mod"){
            // 检查参数
            if(params.empty()){
                cout << "Error: Please provide parameters. Usage: fd-mod {name:\"mod_name\",des:\"description\"}\n";
                continue;
            }
            
            // 传递参数给Python脚本
            string full_cmd = "python3 \"" + py_path + "fd-mod.py\" " + params;
            FILE* pipe = popen(full_cmd.c_str(), "r");
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
            } else {
                cout << "Error: Failed to execute Python script!\n";
            }
        }
        else if(cmd_lower == "fd-block"){
            if(name.empty()){
                cout << "Error: Please create a mod first using 'fd-mod' command!\n";
                continue;
            }
            if(params.empty()){
                cout << "Error: Please provide parameters. Usage: fd-block {name:\"block_name\",des:\"description\",icon:\"texture_name\"}\n";
                continue;
            }
            
            // 传递参数给Python脚本，添加mod名称
            string full_cmd = "python3 \"" + py_path + "fd-block.py\" " + params + ";name=" + name + ";";
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
                cout << "Error: Failed to execute Python script!\n";
            }
        }
        else if(cmd_lower == "fd-item"){
            if(name.empty()){
                cout << "Error: Please create a mod first using 'fd-mod' command!\n";
                continue;
            }
            if(params.empty()){
                cout << "Error: Please provide parameters. Usage: fd-item {name:\"item_name\",des:\"description\",type:\"2d/3d\",texture:\"texture_name\"}\n";
                continue;
            }
            
            // 传递参数给Python脚本，添加mod名称
            string full_cmd = "python3 \"" + py_path + "fd-item.py\" " + params + ";name=" + name + ";";
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
                cout << "Error: Failed to execute Python script!\n";
            }
        }
        else{
            cout << "Unknown command: " << cmd_name << "\n";
            cout << "Type 'help' for available commands.\n";
        }
    }
    return 0;
}

