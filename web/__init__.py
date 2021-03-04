#-*-coding:utf-8-*-

from server import app
from flask import render_template, make_response, request, redirect, abort
import random

def random_str():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt

@app.route('/', methods=['GET'])
def index():
    # headers = request.headers
    # host = headers['Host']
    # if host.startswith('2016'):
    #     return redirect('http://www.aut-video-captions.top/2016')
    # elif host.startswith('2017'):
    #     return redirect('http://www.aut-video-captions.top/2017')
    # elif host.startswith('2020'):
    #     return redirect('http://www.aut-video-captions.top/2020')
    return redirect('/2020')

@app.route('/<year>/', methods=['GET'])
def index_year(year):
    if year != '2016' and year != '2017' and year != '2020' and year != '2021':
        abort(404)
    return render_template('index.%s.html'%year)

@app.route('/people', methods=['GET'])
def people():
    # headers = request.headers
    # host = headers['Host']
    # if host.startswith('2016'):
    #     return redirect('http://www.aut-video-captions.top/2016/people')
    # elif host.startswith('2017'):
    #     return redirect('http://www.aut-video-captions.top/2017/people')
    # elif host.startswith('2020'):
    #     return redirect('http://www.aut-video-captions.top/2020/people')
    return redirect('/2021/people')


@app.route('/<year>/people', methods=['GET'])
def people_year(year):
    if year != '2016' and year != '2017' and year != '2020' and year != '2021':
        abort(404)
    return render_template('people.%s.html'%year)

@app.route('/challenge', methods=['GET'])
def challenge():
    # headers = request.headers
    # host = headers['Host']
    # if host.startswith('2016'):
    #     return redirect('http://www.aut-video-captions.top/2016/challenge')
    # elif host.startswith('2017'):
    #     return redirect('http://www.aut-video-captions.top/2017/challenge')
    # elif host.startswith('2020'):
    #     return redirect('http://www.aut-video-captions.top/2020/challenge')
    return redirect('/2021/challenge')

@app.route('/<year>/challenge', methods=['GET'])
def challenge_year(year):
    if year != '2016' and year != '2017' and year != '2020' and year != '2021':
        abort(404)
    return render_template('challenge.%s.html'%year, random=random_str())

@app.route('/dataset', methods=['GET'])
def dataset():
    # headers = request.headers
    # host = headers['Host']
    # if host.startswith('2016'):
    #     return redirect('http://www.aut-video-captions.top/2016/dataset')
    # elif host.startswith('2017'):
    #     return redirect('http://www.aut-video-captions.top/2017/dataset')
    # elif host.startswith('2020'):
    #     return redirect('http://www.aut-video-captions.top/2020/dataset')
    return redirect('/2021/dataset')

@app.route('/<year>/dataset', methods=['GET'])
def dataset_year(year):
    if year != '2016' and year != '2017' and year != '2020' and year != '2021':
        abort(404)
    return render_template('dataset.%s.html'%year)

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    # headers = request.headers
    # host = headers['Host']
    # if host.startswith('2016'):
    #     return redirect('http://www.aut-video-captions.top/2016/leaderboard')
    # elif host.startswith('2017'):
    #     return redirect('http://www.aut-video-captions.top/2017/leaderboard')
    # elif host.startswith('2020'):
    #     return redirect('http://www.aut-video-captions.top/2020/leaderboard')
    return redirect('/2020/leaderboard')

@app.route('/<year>/leaderboard', methods=['GET'])
def leaderboard_year(year):
    if year != '2016' and year != '2017' and year != '2020' and year != '2021':
        abort(404)
    return render_template('leaderboard.%s.html'%year)

@app.route('/<year>/tmp', methods=['GET'])
def tmp_year(year):
    if year != '2016' and year != '2017' and year != '2020':
        abort(404)
    return render_template('leaderboard.%s.new.html'%year)

@app.route('/tmp', methods=['GET'])
def tmp():
    return redirect('/2020/tmp')


@app.route('/contact', methods=['GET'])
def contact():
    headers = request.headers
    host = headers['Host']
    if host.startswith('2016'):
        return redirect('http://www.aut-video-captions.top/2016/contact')
    elif host.startswith('2017'):
        return redirect('http://www.aut-video-captions.top/2017/contact')
    elif host.startswith('2020'):
        return redirect('http://www.aut-video-captions.top/2020/contact')
    return redirect('/2020/contact')

@app.route('/<year>/team', methods=['GET'])
def team_year(year):
    if year != '2016' and year != '2017' and year != '2020' and year != '2021':
        abort(404)
    return render_template('team.%s.html'%year)


@app.route('/team', methods=['GET'])
def team():
    headers = request.headers
    host = headers['Host']
    if host.startswith('2016'):
        return redirect('http://www.aut-video-captions.top/2016/team')
    elif host.startswith('2017'):
        return redirect('http://www.aut-video-captions.top/2017/team')
    elif host.startswith('2020'):
        return redirect('http://www.aut-video-captions.top/2020/team')
    return redirect('/2020/team')

@app.route('/<year>/contact', methods=['GET'])
def contact_year(year):
    if year != '2016' and year != '2017' and year != '2020':
        abort(404)
    return render_template('contact.%s.html'%year)


@app.route('/browse', methods=['GET'])
def browse():
    args = request.args
    if not 'token' in args:
        return ''
    token = args['token']
    if token == 'msramsmbest':
        return render_template('browse.html')
    else:
        return ''

@app.route('/reset', methods=['GET'])
def reset():
    args = request.args
    if not 'token' in args or not 'challenge_type' in args:
        return ''
    token = args['token']
    challenge_type = args['challenge_type']
    return render_template('reset.html', token=token, challenge_type=challenge_type)
