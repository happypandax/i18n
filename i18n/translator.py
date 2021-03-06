from string import Template

from . import config
from . import resource_loader
from . import translations


class TranslationFormatter(Template):
    delimiter = config.get('placeholder_delimiter')

    def __init__(self, template):
        super(TranslationFormatter, self).__init__(template)

    def format(self, **kwargs):
        if config.get('error_on_missing_placeholder'):
            return self.substitute(**kwargs)
        else:
            return self.safe_substitute(**kwargs)


def t(key, **kwargs):
    locale = kwargs.pop('locale', config.get('locale'))
    if translations.has(key, locale):
        return translate(key, locale=locale, **kwargs)
    else:
        resource_loader.search_translation(key, locale)
        if translations.has(key, locale):
            return translate(key, locale=locale, **kwargs)
        elif locale != config.get('fallback'):
            return t(key, locale=config.get('fallback'), **kwargs)
    if 'default' in kwargs:
        return kwargs['default']
    if config.get('error_on_missing_translation'):
        raise KeyError('key {0} not found'.format(key))
    else:
        return key


def translate(key, **kwargs):
    locale = kwargs.pop('locale', config.get('locale'))
    translation = translations.get(key, locale=locale)
    if isinstance(translation, dict) and 'count' not in kwargs:
        kwargs['count'] = 0
    if 'count' in kwargs:
        translation = pluralize(key, translation, kwargs['count'])
    return TranslationFormatter(translation).format(**kwargs)


def pluralize(key, translation, count):
    return_value = key
    try:
        if type(translation) != dict:
            return_value = translation
            raise KeyError('use of count witouth dict for key {0}'.format(key))
        if count == 0:
            if 'zero' in translation:
                return translation['zero']
            elif 'one' in translation:
                return translation['one']
        elif count == 1:
            if 'one' in translation:
                return translation['one']
            if 'zero' in translation:
                return translation['zero']
        elif count <= config.get('plural_few'):
            if 'few' in translation:
                return translation['few']
            elif 'many' in translation:
                return translation['many']
        elif count > config.get('plural_few'):
            if 'many' in translation:
                return translation['many']
            elif 'few' in translation:
                return translation['few']
        if 'other' in translation:
            return translation['other']
        else:
            raise KeyError('"other" not defined for key {0}'.format(key))
    except KeyError as e:
        if config.get('error_on_missing_plural'):
            raise e
        else:
            return return_value
