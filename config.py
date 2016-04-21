import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    '''Common configuration for different situtations.'''

    SECRET_KEY = os.environ.get('SECRET_KEY') or \
            'EVtH`,}c?K=/cR!l4l?.iqe>n^A<<~Z8qUmt9K3|oZ/>GSK|$Eu7nQC\'o;EIIBB9Xep{<1HTjSY4W!kB*!nwd_c1ryc7LO?/XP60eko}n}]>!T*Zi_[B0H"X"Z@0s)HTu>J`6"wx+]B~"n4IuE@#2|j=:|n7\'dtVR-t?Vb0o2x|ftFq>LNp~\'kul19WS8.yqv@j/4(VeS+_UKs`V{SQ9G}-s6~/qrbFXF[Nwh{H<xXahk}S<EnQrYj3=..Q@/Y?2'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        """Subclass overrides this method to initialize the app instance."""
        pass

    @staticmethod
    def post_init_app(app):
        """Subclass overrides this method to change settings after app
        initialization."""
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    @staticmethod
    def post_init_app(app):
        from flask.ext.bootstrap import WebCDN
        # change flask-bootstrap cdns
        # from flask-bootstrap source code Bootstrap.init_app()
        bootstrapcdn = WebCDN('//libs.useso.com/js/bootstrap/3.2.0/')
        jquery = WebCDN('//libs.useso.com/js/jquery/2.1.1/')
        html5shiv = WebCDN('//libs.useso.com/js/html5shiv/3.7/')
        respondjs = WebCDN('//libs.useso.com/js/respond.js/1.4.2/')
        cdns = {
            'bootstrap': bootstrapcdn,
            'jquery': jquery,
            'html5shiv': html5shiv,
            'respond.js': respondjs,
        }
        app.extensions['bootstrap']['cdns'].update(cdns)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class HerokuConfig(ProductionConfig):

    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,

    'default': DevelopmentConfig,
}
