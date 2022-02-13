console.log('读者你好啊，如果你也是浪漫的人，欢迎联系 henry1911@foxmail.com ~')

const submit = async (e) => {
  e.preventDefault()
  const data = Object.fromEntries(new FormData(e.target))
  const img = await fetch('/generate-photo', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
    },
  })
  const imgBlob = await img.blob()
  const imgUrl = URL.createObjectURL(imgBlob)
  const imgElement = document.getElementById('img')
  imgElement.src = imgUrl
}

const form = document.getElementById('thecoolform')
form.addEventListener('submit', submit)