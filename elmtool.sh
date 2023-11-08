#!/bin/bash
if wget -q --spider http://111.67.195.249:3535/d/%E6%96%87%E4%BB%B6/elmtool/web%E5%8D%87%E7%BA%A7%E7%A8%8B%E5%BA%8F/elmtool.sh; then
    wget -O elmtool.sh http://111.67.195.249:3535/d/%E6%96%87%E4%BB%B6/elmtool/web%E5%8D%87%E7%BA%A7%E7%A8%8B%E5%BA%8F/elmtool.sh
    echo "更新成功"
    # 在这里添加下载文件后的其他操作
else
    echo "更新失败"
    # 在这里添加下载失败或链接失败时的处理逻辑
fi
sleep 3s
clear

# 定义颜色样式
yellow='\033[0;40m'
green='\033[99;32m'
red='\033[1;31m'
NC='\033[0m' # 恢复默认值

# 定义要显示的消息
line1="======================="
line2="|| ${green}本程序为 elmtool 升级程序 ${NC}${yellow}||"
line3="|| ${red}作者:Mr.陈 TG:@wcnmsb123 ${NC}${yellow} ||"
line4="|| ${red}当前版本1.0 ${NC}${yellow} ||"
line5="|| ${red}如需使用本程序请保证配置文件存储于elmWeb文件夹内,上级文件不要求 ${NC}${yellow} ||"
line6="|| ${red}请选择要执行的操作(输入数字1/2/3)：${NC}"
line7="|| ${red}1. 停止并删除容器，再进行升级${NC}"
line8="|| ${red}2. 直接运行拉取镜像和运行容器${NC}\n|| ${red}3. 搭建老虎sign${NC}"
line9="======================="

# 输出文本
echo -e "${yellow}${line1}${NC}"
echo -e "${yellow}${line2}${NC}"
echo -e "${yellow}${line3}${NC}"
echo -e "${yellow}${line4}${NC}"
echo -e "${yellow}${line5}${NC}"
echo -e "${yellow}${line9}${NC}"
sleep 3s
clear
echo -e "${yellow}${line1}${NC}"
echo -e "${yellow}${line6}${NC}"
echo -e "${yellow}${line7}${NC}"
echo -e "${yellow}${line8}${NC}"
echo -e "${yellow}${line9}${NC}"

# 读取用户输入
read -p "请输入数字1/2/3：" choice
function allow_port() {
  local port=$1
  local firewall_type

  # 判断系统中使用的防火墙类型
  if [ -n "$(command -v iptables)" ]; then
    # 如果存在 iptables 命令，则说明使用 iptables
    firewall_type="iptables"
  elif [ -n "$(command -v firewall-cmd)" ]; then
    # 如果存在 firewall-cmd 命令，则说明使用 firewalld
    firewall_type="firewalld"
  else
    # 如果都不存在，则输出错误信息并退出函数
    echo "未找到支持的防火墙类型"
    return 1
  fi

  # 根据防火墙类型进行相应的端口放行操作
  if [ "$firewall_type" = "iptables" ]; then
    # 针对 iptables 的端口放行操作
    echo "端口放行${port}"
    iptables -A INPUT -p tcp --dport "$port" -j ACCEPT
  elif [ "$firewall_type" = "firewalld" ]; then
    # 针对 firewalld 的端口放行操作
    echo "端口放行${port}"
    firewall-cmd --zone=public --add-port="$port/tcp" --permanent
    # 生效配置
    firewall-cmd --reload
  fi
}


# 拉取镜像和创建容器的函数
pull_and_run_container() {
    # 定义镜像名称
    echo "==========安装程序============="
    image_name="marisn/elmweb"

    # 拉取镜像
    #docker pull $image_name
    if [[ $? -ne 0 ]]; then
        echo "拉取镜像出错，脚本退出"
        exit 1
    fi

    # 获取用户输入用于搭建elmtool的容器名称。
    read -p "请输入要用于搭建 elmtool 的容器名称(留空则使用默认名称 elmWeb ):" container_name
    # 如果用户未输入容器名称，则使用默认名称"elmWeb"。
    if [[ -z $container_name ]]; then
        container_name="elmWeb"
    fi

    # 获取用户输入elmWeb的上一级路径，默认为"etc"。
    read -p "请输入 elmWeb 上一级路径(默认 etc ):" lujing_name
    if [[ -z $lujing_name ]]; then
      lujing_name="etc"
    fi
    if [[ ! -d "/$lujing_name/elmWeb" ]]; then
      echo "生成 elmWeb 文件夹"
      mkdir -p "/$lujing_name/elmWeb"
    fi
    # 检查config.ini文件是否存在，如果不存在则创建
    config_file="/$lujing_name/elmWeb/config.ini"
    if [[ ! -f $config_file ]]; then
      echo "生成 config.ini 文件"
      touch $config_file
      read -p "请输入你的授权码(如不想填写可直接回车):" new_auth_code
      if [[ -n $new_auth_code ]]; then
        read -p "请输入你的端口(默认:8081):" duanko
        if [[ -z $duanko ]]; then
          duanko="8081"
        fi
        # 将新的授权码写入config.ini文件中
        echo -e "[basic]\nauth_code = ${new_auth_code}\n[server]\nport =${duanko}" >> $config_file
        echo "授权码已更新为：$new_auth_code"
      else 
          new_auth_code="取消"
      fi
    fi
    
    # 检查database.db文件是否存在，如果不存在则创建
    database_file="/$lujing_name/elmWeb/database.db"
    if [[ ! -f $database_file ]]; then
      echo "生成 database.db 文件"
      touch $database_file
    fi
    # 使用docker run命令运行容器，并挂载配置文件和数据库文件。
    docker run -dit \
      -v /$lujing_name/elmWeb/config.ini:/etc/elmWeb/config.ini \
      -v /$lujing_name/elmWeb/database.db:/etc/elmWeb/database.db \
      --network host \
      --name $container_name \
      --restart unless-stopped \
      $image_name:latest
    if [[ $? -ne 0 ]]; then
        echo "运行容器出错，脚本退出"
        exit 1
    fi
    sleep 3s
    if [[ $new_auth_code != "取消" ]]; then
      allow_port "${duanko}"
      echo "http://127.0.0.1:${duanko}/static/config/config.ini"
      # 将新的授权码写入config.ini文件中
      if wget -q --spider http://127.0.0.1:${duanko}/static/config/config.ini; then
         wget -O /$lujing_name/elmWeb/cc.ini http://127.0.0.1:${duanko}/static/config/config.ini
         echo "如:你刚刚卡密填写无误,请去这个路径/$lujing_name/elmWeb/cc.ini"
         echo "虽可临时使用,但为了体验全部功能还请"
         echo "进行更完整的配置并更改文件名为config.ini"
       # 在这里添加下载文件后的其他操作
      else
          echo "${duanko}端口访问失败"
      fi
    elif [[ $new_auth_code == "取消" ]]; then
        allow_port 8081
        if wget -q --spider http://127.0.0.1:8081/static/config/config.ini; then
          wget -O /$lujing_name/elmWeb/config.ini http://127.0.0.1:8081/static/config/config.ini
          echo "已经为你拉取最新配置文件请前去填写"
          echo "这个是存储路径/$lujing_name/elmWeb/config.ini"
        else
            echo "8081端口访问失败"
        fi
    fi
    
    read -p "是否查看容器日志(y/n):" rz
    if [[ $rz == "y" ]]; then
       docker logs "$container_name"
    fi
}

if [[ $choice -eq 1 ]]; then
    # 获取用户输入，要停止并删除的Docker容器名称
    echo "==========删除程序============="
    read -p "请输入要停止并删除的Docker容器名称:" container_name
    # 停止并删除容器
    docker stop $container_name && docker rm $container_name
    if [[ $? -ne 0 ]]; then
        echo "停止并删除容器出错，脚本退出"
        exit 1
    fi
    read -p "确认删除elmWeb上级路径及其下所有内容？(请输入 'yes' 确认): " confirm
    if [[ $confirm == "yes" ]]; then
        read -p "删除elmWeb文件夹的上级路径: " delete_path
        if [[ -d "/$delete_path/elmWeb" ]]; then
            rm -ri "/$delete_path/elmWeb"
        else
            echo "路径不存在或不是一个目录"
        fi
    else
        echo "取消删除操作"
    fi
    pull_and_run_container
elif [[ $choice -eq 2 ]]; then
    # 调用拉取镜像和创建容器的函数
    pull_and_run_container
elif [[ $choice -eq 3 ]]; then
    # 调用拉取镜像和创建容器的函数
    read -p "老虎sign端口(默认9999):" duanko
    if [[ -z $duanko ]]; then
       duanko=9999
    fi
    allow_port "${duanko}"
    docker run -itd --name eleSign -p ${duanko}:9999 --restart=unless-stopped pingxingsheng/elesign
else
    echo "输入不合法，脚本退出"
    exit 1
fi