/**
 * MFT Shell - 完全重构版本(虽然用了下工具但是原本自己写的主逻辑没有太大改变哦)
 * 重构以下：
 * 
 * 主要改进：
 * 1. 消除全局变量污染
 * 2. 健壮的参数解析
 * 3. 安全的路径处理
 * 4. 统一的错误处理
 * 5. 更好的UTF-8支持
 */

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <cstring>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <algorithm>
#include <chrono>
#include <thread>
#include <regex>
#include <climits>
#include <clocale>

// ============================================================================
// 工具类命名空间
// ============================================================================
namespace utils {
    
    /**
     * @brief 去除字符串两端空白
     */
    std::string trim(const std::string& str) {
        if (str.empty()) return "";
        
        size_t start = 0;
        while (start < str.length() && std::isspace(static_cast<unsigned char>(str[start]))) {
            start++;
        }
        
        size_t end = str.length();
        while (end > start && std::isspace(static_cast<unsigned char>(str[end - 1]))) {
            end--;
        }
        
        return str.substr(start, end - start);
    }
    
    /**
     * @brief 转小写
     */
    std::string toLower(const std::string& str) {
        std::string result = str;
        std::transform(result.begin(), result.end(), result.begin(),
                       [](unsigned char c) { return std::tolower(c); });
        return result;
    }
    
    /**
     * @brief 获取程序路径，原本给GPT写的，后来发现有问题而改
     */
    std::string getProgramPath() {
        char result[PATH_MAX];
        ssize_t count = readlink("/proc/self/exe", result, PATH_MAX);
        
        if (count == -1) {
            return ".";
        }
        
        std::string path(result, count);
        size_t pos = path.find_last_of("/");
        
        if (pos == std::string::npos) {
            return ".";
        }
        
        return path.substr(0, pos);
    }
    
    /**
     * @brief 检查路径是否存在
     */
    bool pathExists(const std::string& path) {
        struct stat st;
        return (stat(path.c_str(), &st) == 0);
    }
    
    /**
     * @brief 确保路径以斜杠结尾
     */
    std::string ensureTrailingSlash(const std::string& path) {
        if (path.empty()) return "./";
        if (path.back() != '/') return path + "/";
        return path;
    }
    
    /**
     * @brief 查找Python脚本路径
     */
    std::string findPythonScriptsPath(const std::string& programPath) {
        std::vector<std::string> searchPaths = {
            programPath + "/../script/py/",
            programPath + "/script/py/",
            "./script/py/",
            "../script/py/",
            "/media/ljz/LJZ/MFT/script/py/"
        };
        
        for (const auto& path : searchPaths) {
            std::string normalized = path;
            // 去除尾部多余斜杠
            while (!normalized.empty() && normalized.back() == '/') {
                normalized.pop_back();
            }
            
            if (pathExists(normalized)) {
                return normalized + "/";
            }
        }
        
        return "";
    }
    
    /**
     * @brief 去除ANSI颜色代码
     */
    std::string stripAnsi(const std::string& str) {
        std::string result;
        bool escape = false;
        
        for (char c : str) {
            if (escape) {
                if (c >= 'A' && c <= 'Z') {
                    escape = false;
                }
            } else if (c == '\033') {
                escape = true;
            } else {
                result += c;
            }
        }
        
        return result;
    }
}

/**
 * @brief 安全的参数解析器
 */
class ParameterParser {
private:
    std::unordered_map<std::string, std::string> params_;
    
public:
    bool parse(const std::string& input) {
        params_.clear();

        if (input.empty()) {
            return true;
        }

        std::vector<std::string> args;
        std::string current;
        bool inQuotes = false;
        char quoteChar = '\0';

        for (size_t i = 0; i < input.length(); ++i) {
            char c = input[i];

            if (inQuotes) {
                if (c == quoteChar) {
                    inQuotes = false;
                    quoteChar = '\0';
                } else {
                    current += c;
                }
            } else {
                if (c == '"' || c == '\'') {
                    inQuotes = true;
                    quoteChar = c;
                } else if (std::isspace(static_cast<unsigned char>(c))) {
                    if (!current.empty()) {
                        args.push_back(current);
                        current.clear();
                    }
                } else {
                    current += c;
                }
            }
        }

        if (!current.empty()) {
            args.push_back(current);
        }

        for (size_t i = 0; i < args.size(); ++i) {
            if (args[i].substr(0, 2) == "--") {
                std::string key = args[i].substr(2);
                if (i + 1 < args.size()) {
                    params_[key] = args[i + 1];
                    ++i; // 跳过值
                } else {
                    // 没有值，设为空
                    params_[key] = "";
                }
            }
        }

        return true;
    }
    
    std::string get(const std::string& key, const std::string& defaultValue = "") const {
        auto it = params_.find(key);
        if (it != params_.end()) {
            return it->second;
        }
        return defaultValue;
    }
    
    int getInt(const std::string& key, int defaultValue = 0) const {
        try {
            return std::stoi(get(key, std::to_string(defaultValue)));
        } catch (...) {
            return defaultValue;
        }
    }
    
    double getDouble(const std::string& key, double defaultValue = 0.0) const {
        try {
            return std::stod(get(key, std::to_string(defaultValue)));
        } catch (...) {
            return defaultValue;
        }
    }
    
    bool has(const std::string& key) const {
        return params_.find(key) != params_.end();
    }
    
    bool empty() const {
        return params_.empty();
    }
    
    std::string toArgString(const std::string& modName = "", const std::string& outPath = "") const {
        std::stringstream ss;

        for (const auto& pair : params_) {
            ss << " --" << pair.first << " \"" << pair.second << "\"";
        }
        if (!modName.empty()) {
            ss << " --name \"" << modName << "\"";
        }

        if (!outPath.empty()) {
            ss << " --out \"" << outPath << "\"";
        }

        return ss.str();
    }
};

/**
 * @brief 配置管理器
 */
class ConfigManager {
private:
    std::string configPath_;
    std::string outputPath_;
    
public:
    ConfigManager(const std::string& path = "config.ini") : configPath_(path) {
        load();
    }
    
    void load() {
        outputPath_ = "output/";
        
        std::ifstream file(configPath_);
        if (!file.is_open()) {
            return;
        }
        
        std::string line;
        while (std::getline(file, line)) {
            line = utils::trim(line);
            
            if (line.empty() || line[0] == '#') continue;
            
            size_t eqPos = line.find('=');
            if (eqPos == std::string::npos) continue;
            
            std::string key = utils::toLower(utils::trim(line.substr(0, eqPos)));
            std::string value = utils::trim(line.substr(eqPos + 1));
            
            if (key == "output_path") {
                outputPath_ = utils::ensureTrailingSlash(value);
            }
        }
        
        file.close();
    }
    
    void save() const {
        std::ofstream file(configPath_);
        if (!file.is_open()) {
            std::cerr << "\033[31m[错误] 无法保存配置到: " << configPath_ << "\033[0m\n";
            return;
        }
        
        file << "[Settings]\n";
        file << "output_path=" << outputPath_ << "\n";
        file.close();
        
    std::cout << "\033[32m[信息] 配置已保存到: " << configPath_ << "\033[0m\n";
    }
    
    const std::string& getOutputPath() const { return outputPath_; }
    
    void setOutputPath(const std::string& path) {
        outputPath_ = utils::ensureTrailingSlash(path);
    }
};

/**
 * @brief 脚本执行器
 */
class ScriptExecutor {
private:
    std::string scriptsPath_;
    
public:
    void setScriptsPath(const std::string& path) {
        scriptsPath_ = utils::ensureTrailingSlash(path);
    }
    
    bool execute(const std::string& scriptName, const std::string& args, std::string& output) const {
        if (scriptsPath_.empty()) {
            output = "Error: Scripts path not configured";
            return false;
        }
        
        std::string scriptPath = scriptsPath_ + scriptName;
        
        if (!utils::pathExists(scriptPath)) {
            output = "Error: Script not found: " + scriptPath;
            return false;
        }
        
        std::string command = "python3 -u \"" + scriptPath + "\" " + args;
        
        FILE* pipe = popen(command.c_str(), "r");
        if (!pipe) {
            output = "Error: Failed to execute command";
            return false;
        }
        
        char buffer[4096];
        std::string result;
        
        while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
            result += buffer;
        }
        
        int status = pclose(pipe);
        
        if (WIFEXITED(status)) {
            output = utils::stripAnsi(result);
            return (WEXITSTATUS(status) == 0);
        }
        
        output = "Error: Script terminated abnormally";
        return false;
    }
};

/**
 * @brief Shell上下文（替代全局变量）
 */
class ShellContext {
private:
    std::string currentModName_;
    bool modCreated_;
    
public:
    ShellContext() : modCreated_(false) {}
    
    void setCurrentModName(const std::string& name) {
        currentModName_ = name;
        modCreated_ = !name.empty();
    }
    
    const std::string& getCurrentModName() const { return currentModName_; }
    
    bool isModCreated() const { return modCreated_; }
    
    void resetMod() {
        currentModName_.clear();
        modCreated_ = false;
    }
};

// ========================================================================
// 主程序
// =========================================================================

void printHelp() {
    std::cout << "\n\033[32m=== MFT Shell Help ===\033[0m\n\n";
    std::cout << "\033[36mfd-mod --name \"mod_name\" --des \"description\"\033[0m\n";
    std::cout << "   创建新的模组并生成manifest.json\n\n";

    std::cout << "\033[36mfd-block --name \"block_name\" --des \"description\" --icon \"texture\" --explosion \"1.0\" --light \"0\"\033[0m\n";
    std::cout << "   向当前模组添加新方块\n\n";

    std::cout << "\033[36mfd-item --name \"item_name\" --des \"description\" --type \"2d/3d\" --texture \"texture\" --edible \"false\" --hand \"sword\"\033[0m\n";
    std::cout << "   向当前模组添加新物品\n\n";

    std::cout << "\033[36msetout --path \"output_path\"\033[0m\n";
    std::cout << "   设置输出路径 (默认: output/)\n\n";
    
    std::cout << "\033[36mhelp\033[0m\n";
    std::cout << "   显示此帮助信息\n\n";

    std::cout << "\033[36mexit\033[0m\n";
    std::cout << "   退出shell\n\n";
    
    std::cout << "\033[33m=== Notes ===\033[0m\n";
    std::cout << "1. Do not add '.png' extension to texture names\n";
    std::cout << "2. Put texture files in textures/blocks/ or textures/items/\n";
    std::cout << "3. You must create a mod before adding blocks or items\n\n";
}

bool handleHelp(const std::string& params) {
    if (!params.empty()) {
        std::string cmd = utils::toLower(utils::trim(params));
    std::cout << "\033[36m帮助: " << params << "\033[0m\n";
    std::cout << "使用'help'无参数查看完整帮助。\n";
        return true;
    }
    
    printHelp();
    return true;
}

bool handleExit(const std::string& params, ConfigManager& config) {
    std::cout << "\n\033[32mSaving configuration...\033[0m\n";
    config.save();
    std::cout << "\033[32mGoodbye!\033[0m\n\n";
    return false;  // 信号退出主循环
}

bool handleSetout(const std::string& params, ConfigManager& config) {
    ParameterParser parser;
    if (!parser.parse(params)) {
        std::cout << "\033[31m[错误] 参数无效\033[0m\n";
        return true;
    }
    
    std::string path = parser.get("path", "");
    if (path.empty()) {
        std::cout << "\033[31m[错误] 缺少路径参数。用法: setout --path \"output_path\"\033[0m\n";
        return true;
    }
    
    std::string oldPath = config.getOutputPath();
    config.setOutputPath(path);
    
    std::cout << "\033[32m输出路径从 '" << oldPath << "' 更改为 '" << config.getOutputPath() << "'\033[0m\n";
    return true;
}

bool handleFdMod(
    const std::string& params,
    ScriptExecutor& executor,
    ShellContext& context
) {
    ParameterParser parser;
    if (!parser.parse(params)) {
        std::cout << "\033[31m[错误] 解析参数失败\033[0m\n";
        return true;
    }
    
    std::string name = parser.get("name", "");
    std::string des = parser.get("des", "");
    
    if (name.empty()) {
        std::cout << "\033[31m[ERROR] Missing 'name' parameter\033[0m\n";
        std::cout << "\033[31mUsage: fd-mod {name:\"mod_name\", des:\"description\"}\033[0m\n";
        return true;
    }
    
    if (des.empty()) {
        std::cout << "\033[31m[错误] 缺少'des'参数\033[0m\n";
        std::cout << "\033[31m用法: fd-mod --name \"mod_name\" --des \"description\"\033[0m\n";
        return true;
    }
    
    std::string args = parser.toArgString("", "");
    std::string output;
    
    if (!executor.execute("fd-mod.py", args, output)) {
        std::cout << "\033[31m[错误] " << output << "\033[0m\n";
        return true;
    }
    
    std::cout << output;
    
    // 提取模组名称
    context.setCurrentModName(name);
    
    std::cout << "\033[32m\n模组创建成功！当前模组: " << name << "\033[0m\n";
    return true;
}

bool handleFdBlock(
    const std::string& params,
    ScriptExecutor& executor,
    ShellContext& context,
    const ConfigManager& config
) {
    if (!context.isModCreated()) {
        std::cout << "\033[31m[错误] 请先使用'fd-mod'命令创建模组！\033[0m\n";
        return true;
    }
    
    ParameterParser parser;
    if (!parser.parse(params)) {
        std::cout << "\033[31m[ERROR] Failed to parse parameters\033[0m\n";
        return true;
    }
    
    std::string name = parser.get("name", "");
    if (name.empty()) {
        std::cout << "\033[31m[ERROR] Missing 'name' parameter\033[0m\n";
        std::cout << "\033[31mUsage: fd-block {name:\"block_name\", des:\"description\", icon:\"texture\"}\033[0m\n";
        return true;
    }
    
    std::string args = parser.toArgString(context.getCurrentModName(), config.getOutputPath());
    // 将block参数添加到args传递给Python脚本
    args += " --block \"" + name + "\"";
    
    std::string output;
    
    if (!executor.execute("fd-block.py", args, output)) {
        std::cout << "\033[31m[错误] " << output << "\033[0m\n";
        return true;
    }
    
    std::cout << output;
    std::cout << "\033[32mBlock created successfully!\033[0m\n";
    return true;
}

bool handleFdItem(
    const std::string& params,
    ScriptExecutor& executor,
    ShellContext& context,
    const ConfigManager& config
) {
    if (!context.isModCreated()) {
        std::cout << "\033[31m[错误] 请先使用'fd-mod'命令创建模组！\033[0m\n";
        return true;
    }
    
    ParameterParser parser;
    if (!parser.parse(params)) {
        std::cout << "\033[31m[ERROR] Failed to parse parameters\033[0m\n";
        return true;
    }
    
    std::string name = parser.get("name", "");
    if (name.empty()) {
        std::cout << "\033[31m[ERROR] Missing 'name' parameter\033[0m\n";
        std::cout << "\033[31mUsage: fd-item {name:\"item_name\", des:\"description\", type:\"2d/3d\", texture:\"texture\"}\033[0m\n";
        return true;
    }
    
    std::string args = parser.toArgString(context.getCurrentModName(), config.getOutputPath());
    // 将item参数添加到args传递给Python脚本
    args += " --item \"" + name + "\"";
    
    std::string output;
    
    if (!executor.execute("fd-item.py", args, output)) {
        std::cout << "\033[31m[ERROR] " << output << "\033[0m\n";
        return true;
    }
    
    std::cout << output;
    std::cout << "\033[32m物品创建成功！\033[0m\n";
    return true;
}

int main() {
    // 本地化
    std::setlocale(LC_ALL, "");
    
    // 初始化
    std::string programPath = utils::getProgramPath();
    
    ConfigManager config("config.ini");
    ScriptExecutor executor;
    ShellContext context;
    
    // 查找Python脚本路径
    std::string scriptsPath = utils::findPythonScriptsPath(programPath);
    
    if (scriptsPath.empty()) {
        std::cerr << "\033[31m[错误] 找不到Python脚本目录！\033[0m\n";
        std::cerr << "\033[31m请确保script/py/目录存在。\033[0m\n";
        return 1;
    }
    
    executor.setScriptsPath(scriptsPath);
    
    // 讨好用户
    std::cout << "\033[32m==========================================\033[0m\n";
    std::cout << "\033[32m      MFT Shell v2.0 - Refactored\033[0m\n";
    std::cout << "\033[32m==========================================\033[0m\n";
    std::cout << "\033[32m[INFO] Scripts path: " << scriptsPath << "\033[0m\n";
    std::cout << "\033[32m[INFO] Output path: " << config.getOutputPath() << "\033[0m\n";
    std::cout << "\n\033[33m输入'help'查看可用命令。\033[0m\n";
    std::cout << "\033[33m记得先创建模组！\033[0m\n\n";
    
    // 主循环到了
    std::string input;
    bool running = true;
    
    while (running) {
        std::cout << "\033[34mMFT> \033[0m";
        
        if (!std::getline(std::cin, input)) {
            // EOF或Ctrl+D
            std::cout << "\n\033[32m再见！\033[0m\n";
            break;
        }
        
        input = utils::trim(input);
        
        if (input.empty()) {
            continue;
        }
        
        // 提取命令和参数
        std::string command;
        std::string params;
        
        size_t spacePos = input.find(' ');
        if (spacePos != std::string::npos) {
            command = input.substr(0, spacePos);
            params = input.substr(spacePos + 1);
        } else {
            command = input;
        }
        
        command = utils::toLower(command);
        
        // 处理命令
        if (command == "help" || command == "h" || command == "?") {
            running = handleHelp(params);
        }
        else if (command == "exit" || command == "quit" || command == "q") {
            running = handleExit(params, config);
        }
        else if (command == "setout") {
            running = handleSetout(params, config);
        }
        else if (command == "fd-mod") {
            running = handleFdMod(params, executor, context);
        }
        else if (command == "fd-block") {
            running = handleFdBlock(params, executor, context, config);
        }
        else if (command == "fd-item") {
            running = handleFdItem(params, executor, context, config);
        }
        else {
            std::cout << "\033[31m[错误] 未知命令: " << command << "\033[0m\n";
            std::cout << "\033[31m输入'help'查看可用命令。\033[0m\n";
        }
    }
    //要用的复杂的函数丢给AI了，其他函数自己重构掉了，所以主程序看起来非常简洁，容易扩展
    return 0;
}

