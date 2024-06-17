import { useState } from 'react'
import './App.css'
import { useTranslation } from 'react-i18next'
import { Button, Upload } from 'antd'
import { InboxOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
const { Dragger } = Upload
function App() {
  const navigate = useNavigate()
  const { t, i18n } = useTranslation()
  const [imageFile, setImageFile] = useState([])
  const changeLanguage = () => {
    i18n.changeLanguage(i18n.language === 'en' ? 'zh' : 'en')
  }
  const [test, setTest] = useState('identify')
  const [loading, setLoading] = useState(false)

  // 图片文件上传
  const imageFileHandleChange = ({ fileList }) => {
    if (fileList.length != 0) {
      // 获取最新文件的文件名
      let fileName = fileList[fileList.length - 1].originFileObj['name']
      // 提取文件名的后缀名
      let fileExtension = fileName
        .substring(fileName.lastIndexOf('.') + 1)
        .toLowerCase()
      // 定义允许的类型
      let fileTypes = ['jpg', 'png']
      // 首先判断文件上传的类型
      if (fileTypes.indexOf(fileExtension) != -1) {
        let flag =
          fileList[fileList.length - 1].originFileObj['size'] / 1024 / 1024 < 50
        // 在判断文件的大小
        if (flag) {
          // 更新文件(限制只能上传一个文件)
          let newFileList = []
          newFileList.push(fileList[fileList.length - 1])
          setImageFile(newFileList)
        } else {
          message.warning('文件大小必须小于50M')
          // 移除文件
          fileList.pop()
        }
      } else {
        message.warning('文件类型不符合')
        // 移除文件
        fileList.pop()
      }
    } else {
      setImageFile(fileList)
    }
  }

  // 检验
  const identify = () => {
    const formData = new FormData()
    // 多个图片
    imageFile.forEach((item) => {
      formData.append('file', item['originFileObj'])
    })
    setLoading(true)
    axios({
      method: 'post',
      url: 'http://127.0.0.1:5000/upload',
      data: formData,
      timeout: 180000,
    })
      .then((res) => {
        setLoading(false)
        navigate('/detail', {
          state: { predicted_text: res.data.predicted_text },
        })
      })
      .catch((err) => {
        setLoading(false)
        console.log(err)
      })
  }

  return (
    <div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'flex-end',
        }}
      >
        <Button size="small" type="primary" onClick={changeLanguage}>
          {i18n.language == 'en' ? 'en' : '中文'}
        </Button>
      </div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          fontWeight: 'bold',
          fontSize: '25px',
          marginTop: '20px',
        }}
      >
        {t('Plant disease identification')}
      </div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'flex-start',
          marginTop: '20px',
          fontSize: '20px',
        }}
      >
        {t('choose your plantient')}
      </div>
      <div style={{ marginTop: '40px' }}>
        <Dragger
          style={{ width: '350px' }}
          action={'http://127.0.0.1:5000/'} //上传地址，填错/不填上传图片的时候都会报错
          listType="picture"
          fileList={imageFile}
          onChange={imageFileHandleChange}
        >
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">{t('ant-upload-text')}</p>
          <p className="ant-upload-hint">{t('ant-upload-hint')}</p>
        </Dragger>
      </div>

      <div
        style={{ display: 'flex', justifyContent: 'center', marginTop: '40px' }}
      >
        <Button
          type="primary"
          disabled={loading}
          style={{ width: '400px' }}
          // onClick={() => {
          //   navigate('/detail')
          // }}
          onClick={() => identify()}
        >
          {/* {t('identify')} */}
          {t(test)}
        </Button>
      </div>
    </div>
  )
}

export default App
