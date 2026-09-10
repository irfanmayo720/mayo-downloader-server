from flask import Flask, jsonify, request
import yt_dlp

app = Flask(__name__)


@app.route('/get_video', methods=['GET'])
def get_video():
  video_url = request.args.get('url')
  if not video_url:
    return jsonify({'error': 'URL is required'}), 400

  try:
    ydl_opts = {'format': 'best', 'noplaylist': True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(video_url, download=False)
      title = info.get('title', 'Video')
      formats_list = []

      for f in info.get('formats', []):
        url = f.get('url')
        if url and f.get('vcodec') != 'none' and f.get('acodec') != 'none':
          quality = (
              f.get('format_note')
              or f.get('resolution')
              or str(f.get('height', ''))
              + 'p'
              or 'Standard'
          )
          formats_list.append({'quality': quality, 'url': url})

      if not formats_list:
        for f in info.get('formats', []):
          if f.get('url'):
            formats_list.append({
                'quality': f.get('format_note')
                or f.get('resolution')
                or 'Standard',
                'url': f.get('url'),
            })

      return jsonify(
          {'status': 'success', 'title': title, 'formats': formats_list}
      )
  except Exception as e:
    return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
