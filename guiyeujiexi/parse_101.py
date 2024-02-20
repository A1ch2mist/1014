
# 定义一个函数来解析CP56Time2a格式的时间
def parse_cp56time2a(byte_data):
    if len(byte_data) != 7:
        raise ValueError("Invalid CP56Time2a data length.")
    
    # 按照大端格式解析字节数据
    milliseconds = (byte_data[0] << 8) + byte_data[1]
    minute = byte_data[2] & 0x3F
    iv_flag = (byte_data[2] & 0x80) >> 7
    hour = byte_data[3] & 0x1F
    su_flag = (byte_data[3] & 0x80) >> 7
    day_of_month = byte_data[4] & 0x1F
    day_of_week = (byte_data[4] & 0xE0) >> 5
    month = byte_data[5] & 0x0F
    year = byte_data[6] & 0x7F
    
    # 构建并返回一个包含解析时间的字典
    parsed_time = {
        'milliseconds': milliseconds,
        'minute': minute,
        'hour': hour,
        'day_of_month': day_of_month,
        'day_of_week': day_of_week,
        'month': month,
        'year': year + 2000,  # 年份是从2000年开始的偏移量
        'su_flag': su_flag,
        'iv_flag': iv_flag
    }
    
    print(f'{year+2000}/{month}/{day_of_month} {hour}:{minute}:{milliseconds}')

    return parsed_time


# 将十六进制列表转换为大端字节序的二进制字符串
def hex_list_to_decimal(hex_list):

    binary_string = ''.join(format(int(byte, 16), '08b') for byte in hex_list[::-1])

    # 解析符号位、指数位和尾数位，并计算十进制小数值
    sign = int(binary_string[0])
    exponent = int(binary_string[1:9], 2) - 127
    fraction = 1 + int(binary_string[9:], 2) / (2 ** 23)
    decimal_value = (-1) ** sign * fraction * (2 ** exponent)

    # 保留小数点后6位，并采取四舍五入的方式
    decimal_value_rounded = round(decimal_value, 6)

    return decimal_value_rounded



#解析控制域
def parse_control_field(control_field,transmode):
    # 将控制域转换成二进制
    control_field2 = int(control_field, 16)
    binary = format(control_field2, '08b')       #format()函数将十进制整数转换成二进制
    print(f'二进制控制域：{binary}')
    
    # 解析控制域
    res=None
    dir=None
    prm=None
    fcb=None
    fcv=None
    acd=None
    dfc=None
    fc=None

    # 非平衡链路传输模式
    if transmode == 1:
        #启动站发送-下行
        if binary[1] == '1':
            res = binary[0]
            print(f'保留位 RES：{res} , (保留位 RES：设置为 0)')

            prm = binary[1]
            print(f'启动标志位 PRM：{prm} , (启动站发送)')

            fcb = binary[2]
            print(f'帧计数位 FCB：{fcb} , (启动站发送与从动站发送一致)')

            fcv = binary[3]
            print(f'帧计数有效位 FCV：{fcv} , (1表示 FCB 有效；0：表示 FCB 无效)')

            fc = int(binary[4:8], 2)    # 二进制转换成十进制
            
            if fc == 0:
                print(f'功能码 FC：{fc} , (启动方向:复位远方链路)')
            elif fc == 3:
                print(f'功能码 FC：{fc} , (启动方向:发送/确认用户数据)')
            elif fc == 4:
                print(f'功能码 FC：{fc} , (启动方向:发送/无回答用户数据)')
            elif fc == 8:
                print(f'功能码 FC：{fc} , (启动方向:访问请求；从动方向)')
            elif fc == 9:
                print(f'功能码 FC：{fc} , (启动方向:请求/响应请求链路状态)')
            elif fc == 10:
                print(f'功能码 FC：{fc} , (启动方向:请求/响应请求 1 级用户数据)')
            elif fc == 11:
                print(f'功能码 FC：{fc} , (启动方向:请求/响应请求 2 级用户数据)')
            else:
                print(f'功能码 FC：{fc} , (启动方向:未知)')

        #从动站发送-上行
        if binary[1] == '0':
            res = binary[0]
            print(f'保留位 RES：{res} , (保留位 RES：设置为 0)')

            prm = binary[1]
            print(f'启动标志位 PRM：{prm} , (从动站发送)')

            acd = binary[2]
            print(f'请求访问位 ACD：：{acd}  , (1：表示配电终端有 1 级数据等待访问；0：表示配电终端无 1 级数据等待访问)')

            dfc = binary[3]
            print(f'数据流控制位 DFC：{dfc} , (1：表示从动站不能接收后续报文；0：表示从动站可以接收后续报文)')
           
            fc = int(binary[4:8], 2)    # 二进制转换成十进制
            
            if fc == 0:
                print(f'功能码 FC：{fc} , (从动方向：确认：认可)')
            elif fc == 1:
                print(f'功能码 FC：{fc} , (从动方向：确认：否定认可)')
            elif fc == 8:
                print(f'功能码 FC：{fc} , (从动方向：响应：用户数据)')
            elif fc == 9:
                print(f'功能码 FC：{fc} , (从动方向：响应：无所请求的用户数据)')
            elif fc == 11:
                print(f'功能码 FC：{fc} , (从动方向：响应：链路状态)')
            else:
                print(f'功能码 FC：{fc} , (从动方向:未知)')


    # 平衡链路传输模式
    if transmode == 2:
        if binary[0] == '0':      #下行
            dir = binary[0]
            print(f'传输方向位 DIR：{dir} , (下行)')

            prm = binary[1]
            if prm == '1':
                print(f'启动标志位 PRM：{prm} , (启动站发送)')
            else:
                print(f'启动标志位 PRM：{prm} , (从动站发送)')

            fcb = binary[2]
            print(f'帧计数位 FCB：{fcb} , (启动站发送与从动站发送一致)')

            fcv = binary[3]
            print(f'帧计数位 FCV：{fcv} , (1表示 FCB 有效；0：表示 FCB 无效)')

            fc = int(binary[4:8], 2)    # 二进制转换成十进制
            if prm == '1':      #启动站发送
                if fc == 0:
                    print(f'功能码 FC：{fc} , (启动方向:复位远方链路)')
                elif fc == 2:
                    print(f'功能码 FC：{fc} , (启动方向:发送/确认链路测试功能)')
                elif fc == 3:
                    print(f'功能码 FC：{fc} , (启动方向:发送/确认用户数据)')
                elif fc == 4:
                    print(f'功能码 FC：{fc} , (启动方向:发送/无回答用户数据)')
                elif fc == 9:
                    print(f'功能码 FC：{fc} , (启动方向:请求/响应请求链路状态)')
                else:
                    print(f'功能码 FC：{fc} , (启动方向:未知)')

            elif prm == '0':    #从动站发送        
                if fc == 0:
                    print(f'功能码 FC：{fc} , (从动方向：确认：认可)')
                elif fc == 1:
                    print(f'功能码 FC：{fc} , (从动方向：确认：否定认可)')
                elif fc == 11:
                    print(f'功能码 FC：{fc} , (从动方向：响应：链路状态)')
                else:
                    print(f'功能码 FC：{fc} , (从动方向:未知)')


            if binary[0] == '1':      #上行
                dir = binary[0]
                print(f'传输方向位 DIR：{dir} , (上行)')

                prm = binary[1]
                if prm == '1':
                    print(f'启动标志位 PRM：{prm} , (启动站发送)')
                else:
                    print(f'启动标志位 PRM：{prm} , (从动站发送)')

                res = binary[2]
                print(f'保留位 RES：{res} , (保留位 RES：设置为 0)')

                dfc = binary[3]
                print(f'数据流控制位 FCV：{dfc} , (1：表示从动站不能接收后续报文；0：表示从动站可以接收后续报文)')

                fc = int(binary[4:8], 2)    # 二进制转换成十进制

                if prm == '1':      #启动站发送
                    if fc == 0:
                        print(f'功能码 FC：{fc} , (启动方向:复位远方链路)')
                    elif fc == 2:
                        print(f'功能码 FC：{fc} , (启动方向:发送/确认链路测试功能)')
                    elif fc == 3:
                        print(f'功能码 FC：{fc} , (启动方向:发送/确认用户数据)')
                    elif fc == 4:
                        print(f'功能码 FC：{fc} , (启动方向:发送/无回答用户数据)')
                    elif fc == 9:
                        print(f'功能码 FC：{fc} , (启动方向:请求/响应请求链路状态)')
                    else:
                        print(f'功能码 FC：{fc} , (启动方向:未知)')

                elif prm == '0':    #从动站发送        
                    if fc == 0:
                        print(f'功能码 FC：{fc} , (从动方向：确认：认可)')
                    elif fc == 1:
                        print(f'功能码 FC：{fc} , (从动方向：确认：否定认可)')
                    elif fc == 11:
                        print(f'功能码 FC：{fc} , (从动方向：响应：链路状态)')
                    else:  
                        print(f'功能码 FC：{fc} , (从动方向:未知)')

    return {
        'RES': res,
        'DIR': dir,
        'PRM': prm,
        'FCB': fcb,
        'FCV': fcv,
        'ACD': acd,
        'DFC': dfc,
        'FC': fc,
    }

# 解析ASDU  
def parse_asdu(message, startbyte):

    type_id = message[startbyte]
    print(f'类型标识符：{type_id}')
    vsq = message[startbyte + 1]
    cot = message[startbyte + 3] + message[startbyte + 2]
    common_address = message[startbyte + 5] + message[startbyte + 4]
    constant_alue_area_code = []
    info_pi = ''
    info_object_address = None        #需要根据数据类型分别处理->279行
    info_elements = None
    info_object_address_list = []     #建立一个新列表，存储信息对象地址，以便最终返回值给外部功能使用->282行
    info_elements_list = []
    info_time_list = []
    actual_value_list = []


    # 解析ASDU类型标识符
    type_id = int(type_id, 16)
    if type_id == 1:
        print(f'类型标识符：{type_id} , 单点信息')
    elif type_id == 3:
        print(f'类型标识符：{type_id} , 双点信息')
    elif type_id == 9:
        print(f'类型标识符：{type_id} , 测量值，归一化值')
    elif type_id == 11:
        print(f'类型标识符：{type_id} , 测量值，标度化值') 
    elif type_id == 13:
        print(f'类型标识符：{type_id} , 测量值，短浮点数')   
    elif type_id == 30:
        print(f'类型标识符：{type_id} , 带CP56Time2a时标的单点信息')
    elif type_id == 31:
        print(f'类型标识符：{type_id} , 带CP56Time2a时标的双点信息')
    elif type_id == 42:
        print(f'类型标识符：{type_id} , 故障事件信息')
    elif type_id == 45:
        print(f'类型标识符：{type_id} , 单点命令')
    elif type_id == 46:
        print(f'类型标识符：{type_id} , 双点命令')       
    elif type_id == 70:
        print(f'类型标识符：{type_id} , 初始化结束')
    elif type_id == 100:
        print(f'类型标识符：{type_id} , 站总召唤命令')
    elif type_id == 101:
        print(f'类型标识符：{type_id} , 电能量召唤命令')
    elif type_id == 103:
        print(f'类型标识符：{type_id} , 时钟同步命令')
    elif type_id == 104:
        print(f'类型标识符：{type_id} , 测试命令')
    elif type_id == 105:
        print(f'类型标识符：{type_id} , 复位进程命令')
    elif type_id == 200:
        print(f'类型标识符：{type_id} , 切换定值区')
    elif type_id == 201:
        print(f'类型标识符：{type_id} , 读定值区号')
    elif type_id == 202:
        print(f'类型标识符：{type_id} , 读参数和定值')
    elif type_id == 203:
        print(f'类型标识符：{type_id} , 写参数和定值')
    elif type_id == 206:
        print(f'类型标识符：{type_id} , 累计量，短浮点数')
    elif type_id == 207:
        print(f'类型标识符：{type_id} , 带 CP56Time2a 时标的累计量，短浮点数')
    elif type_id == 210:
        print(f'类型标识符：{type_id} , 文件传输')
    elif type_id == 211:
        print(f'类型标识符：{type_id} , 软件升级')


    # 解析ASDU可变结构限定词
    print(f'可变结构限定词：{vsq}')
    vsqdec = int(vsq, 16)
    binary_vsq = format(vsqdec, '08b')       #format()函数将十进制整数转换成二进制
    print(f'二进制可变结构限定词：{binary_vsq}')

    if binary_vsq[0] == '1':
        number_of_elements = int(binary_vsq[1:8], 2)    # 二进制转换成十进制
        print(f'SQ=1，信息元素地址连续')
        print(f'N：{number_of_elements} , 信息元素的个数')
    else:
        number_of_elements = int(binary_vsq[1:8], 2)    # 二进制转换成十进制
        print(f'SQ=0，信息元素地址不连续')
        print(f'N：{number_of_elements} , 信息元素的个数')
    

    # 解析ASDU传送原因
    cot = int(cot, 16)
    if cot == 0:
        print(f'传送原因：{cot} , 未用')
    elif cot == 1:
        print(f'传送原因：{cot} , 周期、循环')
    elif cot == 2:
        print(f'传送原因：{cot} , 背景扫描')
    elif cot == 3:
        print(f'传送原因：{cot} , 突发(自发)') 
    elif cot == 4:
        print(f'传送原因：{cot} , 初始化')   
    elif cot == 5:
        print(f'传送原因：{cot} , 请求或者被激活')
    elif cot == 6:
        print(f'传送原因：{cot} , 激活')
    elif cot == 7:
        print(f'传送原因：{cot} , 激活确认')
    elif cot == 8:
        print(f'传送原因：{cot} , 停止激活')
    elif cot == 9:
        print(f'传送原因：{cot} , 停止激活确认')
    elif cot == 10:
        print(f'传送原因：{cot} , 激活终止')
    elif cot == 13:
        print(f'传送原因：{cot} , 文件传输')        
    elif cot == 20:
        print(f'传送原因：{cot} , 响应站召唤')
    elif cot == 44:
        print(f'传送原因：{cot} , 未知的类型标识')
    elif cot == 45:
        print(f'传送原因：{cot} , 未知的传送原因')
    elif cot == 46:
        print(f'传送原因：{cot} , 未知的应用服务数据单元公共地址')
    elif cot == 47:
        print(f'传送原因：{cot} , 未知的信息体对象地址')
    elif cot == 48:
        print(f'传送原因：{cot} , 遥控执行软压板状态错误')
    elif cot == 49:
        print(f'传送原因：{cot} , 遥控执行时间戳错误')
    elif cot == 50:
        print(f'传送原因：{cot} , 遥控执行数字签名认证错误')
    else:
        print(f'cot error')


    # 解析ASDU公共地址
    print(f'公共地址：{common_address}')

    #解析参数特征标识函数
    def parse_cp8(hex_str):
        # 将16进制字符串转换为二进制字符串
        bin_str = bin(int(hex_str, 16))[2:].zfill(8)

        # 解析各个字段
        cont = int(bin_str[0], 2)  # CONT占据第1位
        # res = int(bin_str[1:6], 2)  # 保留位
        cr = int(bin_str[6], 2)     # CR占据第7位
        se = int(bin_str[7], 2)     # S/E占据第8位

        if cont == 0:
            print(f'CONT：{cont} , 无后续')
        elif cont == 1:
            print(f'CONT：{cont} , 有后续')

        if cr == 0:
            print(f'CR：{cr} , 未用')
        elif cr == 1:
            print(f'CR：{cr} , 取消预置')
            
        if se == 0:
            print(f'S/E：{se} , 固化')
        elif se == 1:
            print(f'S/E：{se} , 预置')


    # 解析ASDU信息对象
    # 信息元素地址不连续SQ=0
    if binary_vsq[0] =='0': 

        #总召唤
        if type_id == 100:
            info_object_address = message[startbyte + 7]+message[startbyte + 6]
            print(f'遥信信息对象地址：{info_object_address}') 
            info_elements = message[startbyte + 8 ]
            print(f'召唤限定词 QOI：{info_elements}， <20> 总召唤')
            info_object_address_list.append(info_object_address)
            info_elements_list.append(info_elements)

        #时钟同步/读取
        elif type_id == 103:
            info_object_address = message[startbyte + 7]+message[startbyte + 6]
            print(f'遥信信息对象地址：{info_object_address}') 
            info_elements = message[startbyte + 8 : startbyte + 15 ]
            print(f'时钟同步：时间 {info_elements}')
            info_time = info_elements
            CP56_time = bytes(int(x, 16) for x in info_time)
            parsed_time = parse_cp56time2a(CP56_time)    #返回值为解析后各部分的字典变量
            info_object_address_list.append(info_object_address)
            info_elements_list.append(info_elements)

            #复位进程命令
        elif type_id == 105:
            info_object_address = message[startbyte + 7]+message[startbyte + 6]
            print(f'遥信信息对象地址：{info_object_address}') 
            info_elements = message[startbyte + 8 ]
            print(f'复位进程命令限定词 QRP：{info_elements}， <1> 进程的总复位')
            info_object_address_list.append(info_object_address)
            info_elements_list.append(info_elements)            

        #初始化结束命令
        elif type_id == 70:
            info_object_address = message[startbyte + 7]+message[startbyte + 6]
            print(f'遥信信息对象地址：{info_object_address}') 
            info_elements = message[startbyte + 8 ]
            print(f'复位进程命令限定词 QRP：{info_elements}， <0> 当地电源合上； <1> 当地手动复位； <2> 远方复位')
            info_object_address_list.append(info_object_address)
            info_elements_list.append(info_elements)        

        #测试命令
        elif type_id == 104:
            info_object_address = message[startbyte + 7]+message[startbyte + 6]
            print(f'遥信信息对象地址：{info_object_address}') 
            info_elements = message[startbyte + 8 : startbyte + 9]
            print(f'固定测试字0xAA55：{info_elements}')
            info_object_address_list.append(info_object_address)
            info_elements_list.append(info_elements)

        #故障事件信息未处理
        elif type_id == 42:
            info_object_address = [] 
            info_elements = message[startbyte + 6 :-2]
            print(f'信息对象：{info_elements}')
            info_object_address_list.append(info_object_address)
            info_elements_list.append(info_elements)

        #文件服务未处理
        elif type_id == 210:
            info_object_address = [] 
            info_elements = message[startbyte + 6 :-2]
            gapless_docinfo = ''.join(info_elements)
            print(f'信息对象：{gapless_docinfo}')
            info_object_address_list.append(info_object_address)
            info_elements_list.append(info_elements)

        #电能量召唤命令未处理
        elif type_id == 101:
            info_object_address = message[startbyte + 7]+message[startbyte + 6]
            print(f'遥信信息对象地址：{info_object_address}') 
            info_elements = message[startbyte + 8]
            print(f'电能量命令限定词 QCC(5)：{info_elements}')
            info_object_address_list.append(info_object_address)
            info_elements_list.append(info_elements)

        #不带时标单点信息或双点信息
        if type_id == 1 or type_id == 3:        
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 7 + 3*i ]+message[startbyte + 6 + 3*i ]
                info_elements = message[startbyte + 8 + 3*i ]
                print(f'遥信信息对象 {i+1} 地址：{info_object_address}') 
                print(f'信息元素 {i+1}：{info_elements}')
                #遍历时建立一个新列表，存储信息元素，以便最终返回值给外部功能使用
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)

        #带时标单点信息或双点信息       
        elif type_id == 30 or type_id == 31:
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 7 + 10*i ]+message[startbyte + 6 + 10*i ]
                info_elements = message[startbyte + 8 + 10*i ]
                print(f'遥信信息对象 {i+1} 地址：{info_object_address}') 
                print(f'信息元素 {i+1}：{info_elements}')
                info_time = message[startbyte + 9 + 10*i : startbyte + 16 + 10*i ]
                CP56_time = bytes(int(x, 16) for x in info_time)
                parsed_time = parse_cp56time2a(CP56_time)
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)
                info_time_list.append(parsed_time)

        #遥测信息
        elif type_id == 9:     #归一化值
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 7 + 5*i ]+message[startbyte + 6 + 5*i ]
                info_elements = message[startbyte + 8 + 5*i : startbyte + 11 + 5*i ]        #减去地址后的信息长度
                print(f'遥测信息对象 {i+1} 地址：{info_object_address}') 
                print(f'信息元素 {i+1}：归一化值：{info_elements[:2]}，品质描述词QDS：{info_elements[2]}')
                hex_info_elements = ''.join(info_elements[:2][::-1])
                int_info_elements = int(hex_info_elements, 16)
                print(f'码值：{int_info_elements}')
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)

        elif type_id == 13:     #短浮点数
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 7 + 7*i ]+message[startbyte + 6 + 7*i ]
                info_elements = message[startbyte + 8 + 7*i : startbyte + 13 + 7*i ]
                print(f'遥测信息对象 {i+1} 地址：{info_object_address}') 
                print(f'信息元素 {i+1}：短浮点数：{info_elements[:4]}，品质描述词QDS：{info_elements[4]}')
                actual_value = hex_list_to_decimal(info_elements[:4])
                print(f'实际值：{actual_value}')
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)
                actual_value_list.append(actual_value)

        #遥控信息
        elif type_id == 45 or type_id == 46:     #单点或双点遥控
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 7 + 3*i ]+message[startbyte + 6 + 3*i ]
                info_elements = message[startbyte + 8 + 3*i ]
                print(f'遥控信息对象 {i+1} 地址：{info_object_address}') 
                print(f'信息元素 {i+1}：单/双命令：{info_elements}')
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)

        #不带时标电能量数据报文
        elif type_id == 206:     
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 7 + 7*i ]+message[startbyte + 6 + 7*i ]
                info_elements = message[startbyte + 8 + 7*i : startbyte + 13 + 7*i]
                print(f'电能量数据对象 {i+1} 地址：{info_object_address}') 
                print(f'信息元素 {i+1}：短浮点数：{info_elements[:4]}，品质描述词QDS：{info_elements[4]}')
                actual_value = hex_list_to_decimal(info_elements[:4])
                print(f'实际值：{actual_value}')
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)    
                actual_value_list.append(actual_value)

        #带时标电能量数据报文
        elif type_id == 207:     
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 7 + 14*i ]+message[startbyte + 6 + 14*i ]
                info_elements = message[startbyte + 8 + 14*i : startbyte + 20 + 14*i]
                print(f'电能量数据对象 {i+1} 地址：{info_object_address}') 
                print(f'信息元素 {i+1}：短浮点数：{info_elements[:4]}，品质描述词QDS：{info_elements[4]}，时标 CP56Time2a：{info_elements[5:]}')
                info_time = info_elements[5:]
                CP56_time = bytes(int(x, 16) for x in info_time)
                parsed_time = parse_cp56time2a(CP56_time)    #返回值为解析后各部分的字典变量
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)
                info_time_list.append(parsed_time)

        #切换定值区
        elif type_id == 200:     
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 7 + 1*i ]+message[startbyte + 6 + 1*i ]
                info_elements = message[startbyte + 9 + 1*i ] + message[startbyte + 8 + 1*i ]
                print(f'定值区号：{info_elements}')
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)

        #读取定值区号
        elif type_id == 201:  
            if cot == 6:   #控制方向
                for i in range(number_of_elements):
                    info_object_address = message[startbyte + 7 + 1*i ]+message[startbyte + 6 + 1*i ]
                    info_elements = []
                    print(f'控制方向无信息元素')
                    info_object_address_list.append(info_object_address)
                    info_elements_list.append(info_elements)
            elif cot == 7:   #监视方向
                for i in range(number_of_elements):
                    info_object_address = message[startbyte + 7 + 1*i ]+message[startbyte + 6 + 1*i ]
                    info_elements = message[startbyte + 8 + 1*i: startbyte + 14 + 1*i ]
                    print(f'当前定值区号：{info_elements[:2]}，终端支持的最小定值区号：{info_elements[2:4]}，终端支持的最大定值区号：{info_elements[4:]}')
                    info_object_address_list.append(info_object_address)
                    info_elements_list.append(info_elements)

        #读取参数和定值
        elif type_id == 202:
            if cot == 6:  #控制方向
                if number_of_elements != 0:  #读多个参数和定值
                    constant_alue_area_code = message[startbyte + 7] + message[startbyte + 6]
                    print(f'读取定值区{constant_alue_area_code}中的参数和定值')
                    for i in range(number_of_elements):
                        info_object_address = message[startbyte + 9 + 2*i ]+message[startbyte + 8 + 2*i ]
                        info_elements = []
                        print(f'信息体{i+1}地址：{info_object_address}')
                        info_object_address_list.append(info_object_address)
                        info_elements_list.append(info_elements)
                else:   #读全部参数和定值
                    constant_alue_area_code = message[startbyte + 7]+message[startbyte + 6]
                    info_object_address = []
                    info_elements = []
                    print(f'定值区号：{info_elements}')
                    info_object_address_list.append(info_object_address)
                    info_elements_list.append(info_elements)

            elif cot == 7:  #监视方向
                constant_alue_area_code = message[startbyte + 7] + message[startbyte + 6]
                print(f'上传定值区{constant_alue_area_code}中的参数和定值')
                info_pi = message[startbyte + 8]
                print(f'参数特征标识{info_pi}')
                parse_cp8(info_pi)
                j =0
                for i in range(number_of_elements):
                    info_object_address = message[startbyte + 10 + j]+message[startbyte + 9 +j]
                    print(f'信息体{i+1}地址：{info_object_address}')
                    info_tag = message[startbyte + 11 +j]
                    print(f'tag类型：{info_tag}')
                    info_length = int(message[startbyte + 12 + j], 16)
                    print(f'数据长度：{info_length}')
                    info_elements = message[startbyte + 13 +j: startbyte + 13 + info_length + j]
                    print(f'信息体{i+1}值：{info_elements}')                                             
                    j += info_length + 4
                    info_object_address_list.append(info_object_address)
                    info_elements_list.append(info_elements)

        #写参数和定值
        elif type_id == 203:
            if number_of_elements != 0:  #写多个参数和定值
                constant_alue_area_code = message[startbyte + 7] + message[startbyte + 6]
                print(f'写定值区{constant_alue_area_code}中的参数和定值')
                info_pi = message[startbyte + 8]
                print(f'参数特征标识{info_pi}')
                parse_cp8(info_pi)
                j =0
                for i in range(number_of_elements):
                    info_object_address = message[startbyte + 10 + j]+message[startbyte + 9 +j]
                    print(f'信息体{i+1}地址：{info_object_address}')
                    info_tag = message[startbyte + 11 + j]
                    print(f'tag类型：{info_tag}')
                    info_length = int(message[startbyte + 12 + j], 16)
                    print(f'数据长度：{info_length}')
                    info_elements = message[startbyte + 13+j: startbyte + 13 + info_length + j]
                    print(f'信息体{i+1}值：{info_elements}')                                             
                    j += info_length + 4
                    info_object_address_list.append(info_object_address)
                    info_elements_list.append(info_elements)
            else:
                constant_alue_area_code = message[startbyte + 7] + message[startbyte + 6]
                print(f'固化/撤销写定值区{constant_alue_area_code}中的参数和定值')
                info_pi = message[startbyte + 8]
                print(f'参数特征标识{info_pi}')
                parse_cp8(info_pi)
                info_object_address = []
                # print(f'信息体地址：{info_object_address}')
                info_tag = []
                # print(f'tag类型：{info_tag}')
                info_length = 0
                # print(f'数据长度：{message[startbyte + 11]}')
                info_elements = []
                # print(f'信息体值：{info_elements}')                                             
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)

        #软件升级
        elif type_id == 211:
            info_object_address = message[startbyte + 7] + message[startbyte + 6]
            print(f'软件升级信息对象地址：{info_object_address}')
            info_elements = message[startbyte + 8]
            print(f'命令类型 CTYPE：{info_object_address}')
            if info_elements == '80':
                print(f'软件升级启动')
            elif info_elements == '00':
                print(f'软件升级结束')
            info_object_address_list.append(info_object_address)
            info_elements_list.append(info_elements)


    # 信息元素地址连续SQ=1
    if binary_vsq[0] == '1':
        info_object_address = message[startbyte + 7]+message[startbyte + 6]
        print(f'信息对象起始地址：{info_object_address}')

        #不带时标单点信息或双点信息
        if type_id == 1 or type_id == 3:        
            for i in range(number_of_elements):
                info_elements = message[startbyte + 8 + i ]
                print(f'遥信信息元素{i+1}：{info_elements}')
                #遍历时建立一个新列表，存储信息元素，以便最终返回值给外部功能使用
                info_elements_list.append(info_elements)

        if type_id == 30 or type_id == 31:        
            for i in range(number_of_elements):
                info_elements = message[startbyte + 8 + 8*i ]
                info_time = info_elements[startbyte + 9 + 8*i : startbyte + 16 + 8*i ]
                CP56_time = bytes(int(x, 16) for x in info_time)
                parsed_time = parse_cp56time2a(CP56_time)
                print(f'遥信信息元素{i+1}：{info_elements}')
                #遍历时建立一个新列表，存储信息元素，以便最终返回值给外部功能使用
                info_elements_list.append(info_elements)
                info_time_list.append(parsed_time)
    
        #遥测信息
        elif type_id == 9:     #归一化值
            for i in range(number_of_elements):
                info_elements = message[startbyte + 8 + 3*i : startbyte + 11 + 3*i ]
                print(f'遥测信息元素 {i+1}：归一化值：{info_elements[:2]}，品质描述词QDS：{info_elements[2]}')
                hex_info_elements = ''.join(info_elements[:2][::-1])
                int_info_elements = int(hex_info_elements, 16)
                print(f'码值：{int_info_elements}')
                info_elements_list.append(info_elements)

        elif type_id == 13:     #短浮点数
            for i in range(number_of_elements):
                info_elements = message[startbyte + 8 + 5*i : startbyte + 13 + 5*i ]
                print(f'遥测信息元素 {i+1}：短浮点数：{info_elements[:4]}，品质描述词QDS：{info_elements[4]}')
                actual_value = hex_list_to_decimal(info_elements[:4])
                print(f'实际值：{actual_value}')
                info_elements_list.append(info_elements)
                actual_value_list.append(actual_value)

        #遥控在标准中只提了SQ=0的情形

        #不带时标电能量数据报文
        elif type_id == 206:     
            for i in range(number_of_elements):
                info_elements = message[startbyte + 8 + 5*i : startbyte + 13 + 5*i]
                print(f'电能量数据元素 {i+1}：短浮点数：{info_elements[:4]}，品质描述词QDS：{info_elements[4]}')
                actual_value = hex_list_to_decimal(info_elements[:4])
                print(f'实际值：{actual_value}')
                info_elements_list.append(info_elements)
                actual_value_list.append(actual_value)

        #带时标电能量数据报文
        elif type_id == 207:     
            for i in range(number_of_elements):
                info_elements = message[startbyte + 8 + 12*i : startbyte + 20 + 12*i]
                print(f'电能量数据元素 {i+1}：短浮点数：{info_elements[:4]}，品质描述词QDS：{info_elements[4]}，时标 CP56Time2a：{info_elements[5:]}')
                actual_value = hex_list_to_decimal(info_elements[:4])
                print(f'实际值：{actual_value}')
                info_time = info_elements[5:]
                CP56_time = bytes(int(x, 16) for x in info_time)
                parsed_time = parse_cp56time2a(CP56_time)    #返回值为解析后各部分的字典变量
                info_elements_list.append(info_elements)
                actual_value_list.append(actual_value)

        #切换定值区
        elif type_id == 200:     
            for i in range(number_of_elements):
                info_elements = message[startbyte + 9 + 1*i ] + message[startbyte + 8 + 1*i ]
                print(f'定值区号：{info_elements}')
                info_elements_list.append(info_elements)

    return {
        'type_id': type_id,
        'vsq': vsq,
        'cot': cot,
        'common_address': common_address,
        'info_object_address': info_object_address_list,
        'info_elements': info_elements_list,
    }

def parse_message_101(message, transmode):
    # 将报文分割成各个部分
    parts = message.split()

    # 检查报文的部分数量是否符合预期
    a = len(parts)
    print(f'报文长度：{a}')
    if len(parts) < 6: 
        print("报文格式错误！")
        return
    
    # 101固定帧长格式报文
    if parts[0] == '10':
        # 解析和打印每个部分
        start_symbol = parts[0]
        print(f'起始符：{start_symbol}')

        control_field = parts[1]
        print(f'控制域：{control_field}')
        control = parse_control_field(parts[1], transmode)     #返回值预留给读取控制域使用

        address_field = parts[2:4]
        #print(f'地址域：{address_field}')
        print(f'地址域：{parts[3]+parts[2]}')

        frame_checksum = parts[4]
        print(f'帧校验和：{frame_checksum}')

        end_character = parts[5]
        print(f'结束字符：{end_character}')



    # 101可变帧长格式报文
    if parts[0] == '68':
        # 解析和打印每个部分
        start_symbol1 = parts[0]
        print(f'起始符1：{start_symbol1}')

        message_length1 = parts[1]
        print(f'报文长度1：{message_length1}')
        
        message_length2 = parts[2]
        print(f'报文长度2：{message_length2}')

        start_symbol2 = parts[3]
        print(f'起始符2：{start_symbol2}')

        control_field = parts[4]
        print(f'控制域：{control_field}')
        control = parse_control_field(parts[4], transmode)     #返回值预留给读取控制域使用

        address_field = parts[5:7]
        gapless_address_field = ''.join(parts[2:6])
        print(f'控制域：{gapless_address_field}')
        #print(f'地址域：{address_field}')
        print(f'地址域：{parts[6]+parts[5]}')

        message_asdu = parts[7:-2]
        gapless_asdu = ''.join(parts[7:-2])
        # print(f'应用服务数据单元：{gapless_asdu}')
        # print(f'应用服务数据单元：{message_asdu}')
        startbyte = 7
        asdu = parse_asdu(parts, startbyte)         #返回值预留给读取ASDU使用
        # print(f'类型标识符：{asdu["type_id"]}')
        # print(f'可变结构限定词：{asdu["vsq"]}')
        # print(f'传送原因：{asdu["cot"]}')
        # print(f'公共地址：{asdu["common_address"]}')
        # print(f'信息对象地址：{asdu["info_object_address"]}')
        # print(f'信息元素：{asdu["info_elements"]}')
        
        frame_checksum = parts[-2]
        print(f'帧校验和：{frame_checksum}')

        end_character = parts[-1]
        print(f'结束字符：{end_character}')


if __name__ == '__main__':
    # 主循环
    while True:
        transmode = 2       # 1:非平衡传输模式， 2:平衡传输模式
        message = input('请输入报文（输入0结束）：')
        if message == '0':
            break
        parse_message_101(message, transmode)
