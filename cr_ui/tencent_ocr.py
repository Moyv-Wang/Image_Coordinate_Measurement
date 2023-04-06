import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
import base64
def tencentOCR(base64img):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential("AKIDLVO0LPDk7GD1ZrsjRvARRO9erqY0B5j9", "jCSTFoBPO7bqqlV0GHDwSijageR3awqa")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.GeneralBasicOCRRequest()
        params = {
            "ImageBase64": base64img
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个GeneralBasicOCRResponse的实例，与请求对象对应
        resp = client.GeneralBasicOCR(req)
        # 输出json格式的字符串回包
        res = resp.to_json_string()
        dic = json.loads(res)
        detected_text = dict['TextDetections'][0]['DetectedText']
        return detected_text


    except TencentCloudSDKException as err:
        print(err)

def image_to_base64(file_path):
    # image转base64
    with open(file_path, "rb") as f:  # 转为二进制格式
        base64_data = base64.b64encode(f.read())  # 使用base64进行加密
        return str(base64_data, encoding="utf-8")
        # file = open('res.txt', 'wt')
        # file.write(str(base64_data, encoding="utf-8"))
        # file.close()