from fastapi.responses import JSONResponse

from configs import messages
from utils.log_utils import put_error


def get_messages(request, exc):
    code = None
    err_message = None
    types = ["integer", "str", "decimal"]
    parms = {}

    if request.query_params is not None:
        parms.update(request.query_params)

    if request.path_params is not None:
        parms.update(request.path_params)

    if exc.body is not None:
        parms.update({"body": exc.body})

    for e in exc.errors():
        errors = e['type'].split('.')

        # bodyが送られてこない場合、bodyが複数件の場合
        if len(e['loc']) == 1:
            code = "ME0010"
            err_message = messages.ME0010
            break
        else: 
            parm, name = e['loc']
            item_name = " (" + str(name) + ")"

        # nullの場合と送られてこない場合
        if(errors[len(errors)-2] == "none" or errors[len(errors)-1] == "missing"):
            code = "ME0012"
            err_message = messages.ME0012 + item_name

        # stringの【""】チェック
        elif(errors[len(errors)-2] == "any_str" and ('ctx' in e and e['ctx']['limit_value'] == 1)):
            code = "ME0012"
            err_message = messages.ME0012 + item_name

        # タイプが正しくない場合
        if(errors[len(errors)-1] in types):
            code = "ME0013"
            err_message = messages.ME0013 + item_name

    response = {'status_code': code, 'message': err_message}

    # ログにエラー情報を保存する
    put_error(response)

    return JSONResponse(
        status_code=400,
        content=response
    )
