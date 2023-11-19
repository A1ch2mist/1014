#最终目标，建造一个报文解析类，拥有分离并解析每个部分的功能，并返回各个部分的值，供外部调用


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

    if transmode == 1:
    # 非平衡链路传输模式
        if binary[0] == '0':
            res = binary[0]
            print(f'保留位 RES：{res} , (保留位 RES：设置为 0)')

            prm = binary[1]
            if prm == '1':
                print(f'启动标志位 PRM：{prm} , (主站发送)')
            else:
                print(f'启动标志位 PRM：{prm} , (从站发送)')

            fcb = binary[2]
            print(f'帧计数位 FCB：{fcb} , (主站发送与从站发送一致)')

            fcv = binary[3]
            print(f'帧计数位 FCV：{fcv} , (1表示 FCB 有效；0：表示 FCB 无效)')

            fc = int(binary[4:8], 2)    # 二进制转换成十进制
            if fc == 0:
                print(f'功能码 FC：{fc} , (启动方向:复位远方链路；从动方向：<0>确认：认可 <1>确认：否定认可)')
            elif fc == 1:
                print(f'功能码 FC：{fc} , (启动方向:复位用户进程；从动方向：<0>确认：认可 <1>确认：否定认可)')
            elif fc == 3:
                print(f'功能码 FC：{fc} , (启动方向:发送/确认用户数据；从动方向：<0>确认：认可 <1>确认：否定认可)')
            elif fc == 4:
                print(f'功能码 FC：{fc} , (启动方向:发送/无回答用户数据；从动方向：无回答)')
            elif fc == 8:
                print(f'功能码 FC：{fc} , (启动方向:访问请求；从动方向：<11>响应：链路状态)')
            elif fc == 9:
                print(f'功能码 FC：{fc} , (启动方向:请求/响应请求链路状态；从动方向：<11>响应：链路状态)')
            elif fc == 10:
                print(f'功能码 FC：{fc} , (启动方向:请求/响应请求 1 级用户数据；从动方向：<8>响应：用户数据 <9>响应：无所请求的用户数据)')
            elif fc == 11:
                print(f'功能码 FC：{fc} , (启动方向:请求/响应请求 2 级用户数据；从动方向：<8>响应：用户数据 <9>响应：无所请求的用户数据)')


        if binary[0] == '1':
            res = binary[0]
            print(f'传输方向位 DIR：{res} , (保留位 RES：设置为 0)')

            prm = binary[1]
            if prm == '1':
                print(f'启动标志位 PRM：{prm} , (主站发送)')
            else:
                print(f'启动标志位 PRM：{prm} , (从站发送)')

            acd = binary[2]
            print(f'帧计数位 FCB：：{acd}  , (ACD=1 表示配电终端有 1 级数据等待访问；ACD=0 表示配电终端无 1 级数据等待访问)')

            dfc = binary[3]
            print(f'帧计数位 FCV：{dfc} , (1：表示从动站不能接收后续报文；0：表示从动站可以接收后续报文)')

            fc = int(binary[4:8], 2)    # 二进制转换成十进制
            if fc == 0:
                print(f'功能码 FC：{fc} , (启动方向:复位远方链路；从动方向：<0>确认：认可 <1>确认：否定认可)')
            elif fc == 1:
                print(f'功能码 FC：{fc} , (启动方向:复位用户进程；从动方向：<0>确认：认可 <1>确认：否定认可)')
            elif fc == 3:
                print(f'功能码 FC：{fc} , (启动方向:发送/确认用户数据；从动方向：<0>确认：认可 <1>确认：否定认可)')
            elif fc == 4:
                print(f'功能码 FC：{fc} , (启动方向:发送/无回答用户数据；从动方向：无回答)')
            elif fc == 8:
                print(f'功能码 FC：{fc} , (启动方向:访问请求；从动方向：<11>响应：链路状态)')
            elif fc == 9:
                print(f'功能码 FC：{fc} , (启动方向:请求/响应请求链路状态；从动方向：<11>响应：链路状态)')
            elif fc == 10:
                print(f'功能码 FC：{fc} , (启动方向:请求/响应请求 1 级用户数据；从动方向：<8>响应：用户数据 <9>响应：无所请求的用户数据)')
            elif fc == 11:
                print(f'功能码 FC：{fc} , (启动方向:请求/响应请求 2 级用户数据；从动方向：<8>响应：用户数据 <9>响应：无所请求的用户数据)')


    if transmode == 2:
        # 平衡链路传输模式
            if binary[0] == '0':      #下行
                dir = binary[0]
                print(f'传输方向位 DIR：{dir} , (下行)')

                prm = binary[1]
                if prm == '1':
                    print(f'启动标志位 PRM：{prm} , (主站发送)')
                else:
                    print(f'启动标志位 PRM：{prm} , (从站发送)')

                fcb = binary[2]
                print(f'帧计数位 FCB：{fcb} , (主站发送与从站发送一致)')

                fcv = binary[3]
                print(f'帧计数位 FCV：{fcv} , (1表示 FCB 有效；0：表示 FCB 无效)')

                fc = int(binary[4:8], 2)    # 二进制转换成十进制
                if fc == 0:
                    print(f'功能码 FC：{fc} , (启动方向:复位远方链路；从动方向：<0>确认：认可 <1>确认：否定认可)')
                elif fc == 1:
                    print(f'功能码 FC：{fc} , (启动方向:复位用户进程；从动方向：<0>确认：认可 <1>确认：否定认可)')
                elif fc == 2:
                    print(f'功能码 FC：{fc} , (启动方向:发送/确认链路测试功能；从动方向：<0>确认：认可 <1>确认：否定认可)')
                elif fc == 3:
                    print(f'功能码 FC：{fc} , (启动方向:发送/确认用户数据；从动方向：<0>确认：认可 <1>确认：否定认可)')
                elif fc == 4:
                    print(f'功能码 FC：{fc} , (启动方向:发送/无回答用户数据；从动方向：无回答)')
                elif fc == 9:
                    print(f'功能码 FC：{fc} , (启动方向:请求/响应请求链路状态；从动方向：<11>响应：链路状态)')


            if binary[0] == '1':      #上行
                dir = binary[0]
                print(f'传输方向位 DIR：{dir} , (上行)')

                prm = binary[1]
                if prm == '1':
                    print(f'启动标志位 PRM：{prm} , (主站发送)')
                else:
                    print(f'启动标志位 PRM：{prm} , (从站发送)')

                res = binary[2]
                print(f'帧计数位 FCB：：{res} , (保留位 RES：设置为 0)')

                dfc = binary[3]
                print(f'帧计数位 FCV：{dfc} , (1：表示从动站不能接收后续报文；0：表示从动站可以接收后续报文)')

                fc = int(binary[4:8], 2)    # 二进制转换成十进制
                if fc == 0:
                    print(f'功能码 FC：{fc} , (启动方向:复位远方链路；从动方向：<0>确认：认可 <1>确认：否定认可)')
                elif fc == 1:
                    print(f'功能码 FC：{fc} , (启动方向:复位用户进程；从动方向：<0>确认：认可 <1>确认：否定认可)')
                elif fc == 2:
                    print(f'功能码 FC：{fc} , (启动方向:发送/确认链路测试功能；从动方向：<0>确认：认可 <1>确认：否定认可)')
                elif fc == 3:
                    print(f'功能码 FC：{fc} , (启动方向:发送/确认用户数据；从动方向：<0>确认：认可 <1>确认：否定认可)')
                elif fc == 4:
                    print(f'功能码 FC：{fc} , (启动方向:发送/无回答用户数据；从动方向：无回答)')
                elif fc == 9:
                    print(f'功能码 FC：{fc} , (启动方向:请求/响应请求链路状态；从动方向：<11>响应：链路状态)')

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


def parse_asdu(message, startbyte):
    # 解析ASDU   
    type_id = message[startbyte]
    print(f'类型标识符：{type_id}')
    vsq = message[startbyte + 1]
    cot = message[startbyte + 2]
    common_address = message[startbyte + 4]+message[startbyte + 3]
    info_object_address = None        #需要根据数据类型分别处理->279行
    info_elements = None
    info_object_address_list = []     #建立一个新列表，存储信息对象地址，以便最终返回值给外部功能使用->282行
    info_elements_list = []


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
    elif type_id == 45:
        print(f'类型标识符：{type_id} , 单点命令')
    elif type_id == 46:
        print(f'类型标识符：{type_id} , 双点命令')
    elif type_id == 55:
        print(f'类型标识符：{type_id} , 预置/激活参数命令')
    elif type_id == 108:
        print(f'类型标识符：{type_id} , 读参数命令')        
    elif type_id == 70:
        print(f'类型标识符：{type_id} , 初始化结束')
    elif type_id == 100:
        print(f'类型标识符：{type_id} , 召唤命令')
    elif type_id == 103:
        print(f'类型标识符：{type_id} , 时钟同步及读取命令')
    elif type_id == 104:
        print(f'类型标识符：{type_id} , 测试命令')
    elif type_id == 105:
        print(f'类型标识符：{type_id} , 复位进程命令')
    #print(f'类型标识符：{type_id}')

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
    #print(f'传送原因：{cot}')

    # 解析ASDU公共地址
    print(f'公共地址：{common_address}')

    # 解析ASDU信息对象地址
    # 信息元素地址连续SQ=1
    if binary_vsq[0] == '1':
        info_object_address = message[startbyte + 6]+message[startbyte + 5]
        # info_object_address_list = []
        # info_object_address_list.append(info_object_address)
        print(f'信息对象起始地址：{info_object_address}')


        #总召唤
        if type_id == 100:
            info_elements = message[startbyte + 7 ]
            print(f'总召唤：{info_elements}')
            info_elements_list.append(info_elements)

        #时钟同步/读取
        elif type_id == 103:
            info_elements = message[startbyte + 7 : startbyte + 14 ]
            print(f'时钟同步：时间 {info_elements}')
            info_elements_list.append(info_elements)

         #复位进程命令
        elif type_id == 105:
            info_elements = message[startbyte + 7 ]
            print(f'复位：{info_elements}， <1> 进程的总复位')
            info_elements_list.append(info_elements)            

        #初始化结束命令
        elif type_id == 70:
            info_elements = message[startbyte + 7 ]
            print(f'初始化原因：{info_elements}， <0> 当地电源合上； <1> 当地手动复位； <2> 远方复位')
            info_elements_list.append(info_elements)        

        #测试命令
        elif type_id == 104:
            info_elements = message[startbyte + 7 : startbyte + 8]
            print(f'固定测试字0Xaa55：{info_elements}')
            info_elements_list.append(info_elements)        

        #不带时标单点信息或双点信息
        elif type_id == 1 or type_id == 3:        
            for i in range(number_of_elements):
                info_elements = message[startbyte + 7 + i ]
                print(f'遥信信息元素{i+1}：{info_elements}')
                #遍历时建立一个新列表，存储信息元素，以便最终返回值给外部功能使用
                info_elements_list.append(info_elements)
        #带时标单点信息或双点信息：按照 DL/T 634.5101-2002 规定，带长时标的单/双点信息遥信报文并不存在信息元素序列（SQ=1）的情况。
       
        #遥测信息
        elif type_id == 9:     #归一化值
            for i in range(number_of_elements):
                info_elements = message[startbyte + 7 + 3*i : startbyte + 10 + 3*i ]
                print(f'遥测信息元素 {i+1}：归一化值：{info_elements[:2]}，品质描述词QDS：{info_elements[2]}')
                info_elements_list.append(info_elements)

        elif type_id == 13:     #短浮点数
            for i in range(number_of_elements):
                info_elements = message[startbyte + 7 + 5*i : startbyte + 12 + 5*i ]
                print(f'遥测信息元素 {i+1}：短浮点数：{info_elements[:4]}，品质描述词QDS：{info_elements[4]}')
                info_elements_list.append(info_elements)

        #遥控在标准中只提了SQ=0的情形

        #读取参数
        elif type_id == 108:     
            for i in range(number_of_elements):
                info_elements = message[startbyte + 7 + 4*i : startbyte + 11 + 4*i ]
                print(f'参数信息元素 {i+1}：短浮点数：{info_elements[:4]}')
                info_elements_list.append(info_elements)

        #预置/激活参数
        elif type_id == 55:     
            for i in range(number_of_elements):
                info_elements = message[startbyte + 7 + 5*i : startbyte + 12 + 5*i ]
                print(f'参数信息元素 {i+1}：短浮点数：{info_elements[:4]}， 设定命令限定词QOS：{info_elements[4]}')     #品质QOS=10000000=0x80，表示预置参数，QOS=00000000=0x00，表示执行激活参数
                info_elements_list.append(info_elements)


    # 信息元素地址不连续SQ=0
    if binary_vsq[0] =='0':      
        #不带时标单点信息或双点信息
        if type_id == 1 or type_id == 3:        
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 6 + 3*i ]+message[startbyte + 5 + 3*i ]
                info_elements = message[startbyte + 7 + 3*i ]
                print(f'遥信信息对象 {i+1} 地址：{info_object_address}') 
                print(f'信息元素 {i+1}：{info_elements}')
                #遍历时建立一个新列表，存储信息元素，以便最终返回值给外部功能使用
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)

        #带时标单点信息或双点信息       
        elif type_id == 30 or type_id == 31:
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 6 + 10*i ]+message[startbyte + 5 + 10*i ]
                info_elements = message[startbyte + 7 + 10*i ]
                print(f'遥信信息对象 {i+1} 地址：{info_object_address}') 
                print(f'信息元素 {i+1}：{info_elements}')
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)

        #遥测信息
        elif type_id == 9:     #归一化值
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 6 + 5*i ]+message[startbyte + 5 + 5*i ]
                info_elements = message[startbyte + 7 + 5*i : startbyte + 10 + 5*i ]        #减去地址后的信息长度
                print(f'遥测信息对象 {i+1} 地址：{info_object_address}') 
                print(f'信息元素 {i+1}：归一化值：{info_elements[:2]}，品质描述词QDS：{info_elements[2]}')
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)

        elif type_id == 13:     #短浮点数
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 6 + 7*i ]+message[startbyte + 5 + 7*i ]
                info_elements = message[startbyte + 7 + 7*i : startbyte + 12 + 7*i ]
                print(f'遥测信息对象 {i+1} 地址：{info_object_address}') 
                print(f'信息元素 {i+1}：短浮点数：{info_elements[:4]}，品质描述词QDS：{info_elements[4]}')
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)

        #遥控信息
        elif type_id == 45 or type_id == 46:     #单点或双点遥控
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 6 + 3*i ]+message[startbyte + 5 + 3*i ]
                info_elements = message[startbyte + 7 + 3*i ]
                print(f'遥控信息对象 {i+1} 地址：{info_object_address}') 
                print(f'信息元素 {i+1}：单/双命令：{info_elements}')
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)

        #读取参数
        elif type_id == 108:
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 6 + 6*i ]+message[startbyte + 5 + 6*i ]
                info_elements = message[startbyte + 7 + 6*i : startbyte + 11 + 6*i ]
                print(f'参数信息对象 {i+1} 地址 ：{info_object_address}') 
                print(f'信息元素 {i+1}：短浮点数：{info_elements[:4]}')     #需要转换为浮点数存储
                info_object_address_list.append(info_object_address)
                info_elements_list.append(info_elements)

        #预置/激活参数
        elif type_id == 55:
            for i in range(number_of_elements):
                info_object_address = message[startbyte + 6 + 7*i ]+message[startbyte + 5 + 7*i ]
                info_elements = message[startbyte + 7 + 7*i : startbyte + 12 + 7*i ]
                print(f'参数信息对象 {i+1} 地址 ：{info_object_address}') 
                print(f'信息元素 {i+1}：短浮点数：{info_elements[:4]}， 设定命令限定词QOS：{info_elements[4]}')     #需要转换为浮点数存储
                info_object_address_list.append(info_object_address)    #品质QOS=10000000=0x80，表示预置参数，QOS=00000000=0x00，表示执行激活参数
                info_elements_list.append(info_elements)        




        








    







 

    
    # print(f'信息对象地址：{info_object_address}')
    # print(f'信息元素：{info_elements}')

    return {
        'type_id': type_id,
        'vsq': vsq,
        'cot': cot,
        'common_address': common_address,
        'info_object_address': info_object_address,
        'info_elements': info_elements,
    }

def parse_message(message, transmode):
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
        #print(f'地址域：{address_field}')
        print(f'地址域：{parts[6]+parts[5]}')

        message_asdu = parts[7:-2]
        gapless_asdu = ''.join(parts[7:-2])
        print(f'应用服务数据单元：{gapless_asdu}')
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



# 主循环
while True:
    transmode = 2       # 1:非平衡传输模式， 2:平衡传输模式
    message = input('请输入报文（输入0结束）：')
    if message == '0':
        break
    parse_message(message, transmode)
