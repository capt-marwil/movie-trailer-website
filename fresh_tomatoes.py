import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            height: 700px;
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        .media-info {
            font-size: 75%;
            font-weight: normal;
            color: #333;
            }
        .media-tabs{
            margin: 20px;
            display-type: block;
            }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile:visible', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
            'visible': 'true',
            'id': 'trailer-video',
            'type': 'text-html',
            'src': sourceUrl,
            'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads and check wether tab is visible
        $(document).ready(function () {
            $('.tab-content:visible').animate(function() {
                $('.movie-tile').hide().first().show("fast", function showNext() {
                    $(this).next("div").show("fast", showNext);
                });
            });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie, Games and TV Show Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
    <div class="media-tabs">
    <ul class="nav nav-tabs">
        <li class="active"><a data-toggle="tab" href="#sectionA">Movies</a></li>
        <li><a data-toggle="tab" href="#sectionB">TV Shows</a></li>
        <li><a data-toggle="tab" href="#sectionC">Games</a></li>
    </ul>
    <div class="tab-content">
        <div id="sectionA" class="tab-pane fade in active">
            <h3>Movies</h3>
            <p>{movie_tiles}</p>
        </div>
        <div id="sectionB" class="tab-pane fade">
            <h3>TV Shows</h3>
            <p>{tv_show_tiles}</p>
        </div>
        <div id="sectionC" class="tab-pane fade">
            <h3>Games</h3>
            <p>{game_tiles}</p>
        </div>
    </div>
    </div>
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal"
 data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h3>{movie_title}</h3>
    <div>{movie_storyline}</div>
    <h4>Director</h4>
    <div class="media-info">{director}</div>
    <h4>Cast</</h4>
    <div class="media-info">{movie_cast}</div>
    <h4>Synopsis</h4>
    <div class="media-info">{movie_synopsis}</div>
   </div>
'''
# A single tv show entry html template
tv_show_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal"
 data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h3>{tv_show_title}</h3>
    <h4>TV Station</h4>
    <div>{tv_show_station}</div>
    <h4>Cast</</h4>
    <div class="media-info">{tv_show_cast}</div>
    <h4>Synopsis</h4>
    <div class="media-info">{tv_show_synopsis}</div>
</div>
'''

game_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal"
 data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h3>{game_title}</h3>
    <h4>Platform</</h4>
    <div class="media-info">{game_platform}</div>
    <h4>Synopsis</h4>
    <div class="media-info">{game_synopsis}</div>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            movie_storyline=movie.movie_storyline,
            poster_image_url=movie.poster_image_url,
            director=movie.director,
            trailer_youtube_id=trailer_youtube_id,
            movie_synopsis=movie.synopsis,
            movie_cast=movie.get_cast()
        )
    return content


def create_tv_show_tiles_content(tv_shows):
    # The HTML content for this section of the page
    content = ''
    for tv_show in tv_shows:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', tv_show.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', tv_show.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the tv show with its content filled in
        content += tv_show_tile_content.format(
            tv_show_title=tv_show.title,
            poster_image_url=tv_show.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            tv_show_station=tv_show.tv_station,
            tv_show_synopsis=tv_show.synopsis,
            tv_show_cast=tv_show.get_cast()
        )
    return content


def create_game_tiles_content(games):
    # The HTML content for this section of the page
    content = ''
    for game in games:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', game.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', game.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the tv show with its content filled in
        content += game_tile_content.format(
            game_title=game.title,
            poster_image_url=game.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            game_synopsis=game.synopsis,
            game_platform=game.get_platform()
        )
    return content


def open_movies_page(movies, tv_shows, games):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the placeholder for the movie tiles, tv show tiles and games tiles
    # with the actual dynamically generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies),
        tv_show_tiles=create_tv_show_tiles_content(tv_shows),
        game_tiles=create_game_tiles_content(games)
        )

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser
    url = os.path.abspath(output_file.name)
    # open in a new tab, if possible
    webbrowser.open('file://' + url, new=2)
