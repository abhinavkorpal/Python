import tempfile
import boto3
from PIL import Image
from chalice import Chalice

app = Chalice(app_name='s3-thumbnail')
app.debug = True
s3 = boto3.client('s3')

@app.on_s3_event(bucket='abhinav-chalice-s3-thumbnail',
                 prefix='images/', suffix='.jpg')
def handler(event):
    app.log.debug("Resize image for: s3://%s/%s",
                  event.bucket, event.key)
    with tempfile.NamedTemporaryFile('w') as f:
        s3.download_file(event.bucket, event.key, f.name)
        with Image.open(f.name) as img:
            img.thumbnail((256, 256))
            out_filename = f.name + '.thumbnail.jpg'
            img.save(out_filename)
    s3.upload_file(out_filename, event.bucket,
                   f'thumbnails/{event.key.split('/', 1)[1]}')