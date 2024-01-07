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

# 解析示例字节数据
info_time = input("请输入时间：")
byte_data_example = bytes(int(x, 16) for x in info_time.split())
parsed_time_example = parse_cp56time2a(byte_data_example)
