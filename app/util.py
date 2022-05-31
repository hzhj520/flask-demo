from flask import jsonify, Response, request
import json


# 返回格式
def api_result(code=None, items=None, total=None, message=None, status=None):
    result = {
        "code": code,
        "message": message,
        "data": {
            "total": total,
            "items": items
        },
    }

    if not items:
        result.pop('data')
    # return jsonify(result)
    # return result
    return jsonify(result)


def api_result_data(code=None, data=None, message=None, status=None):
    result = {
        "code": code,
        "message": message,
        "data": data,
    }

    if not data:
        result.pop('data')
    # return jsonify(result)
    # return result
    return Response(json.dumps(result), content_type='application/json')
    # return jsonify(result)


def request_parse(req_data: request):
    '''解析请求数据并以json形式返回'''
    print(req_data)
    if req_data.method == 'POST':
        print('进入 POST 请求')
        # print(dir(req_data))
        print('req_data.json的内容为-------->', req_data.json)
        data = req_data.json
    elif req_data.method == 'GET':
        print('进入 GET 请求')
        data = req_data.args
    print("本次请求所携带的参数为----------->", data)
    return data


def error(message):
    return jsonify({'success': False, 'message': message})
