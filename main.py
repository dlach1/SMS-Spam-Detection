import math
import re

TRAINING_SET_RATIO = 0.7
TOTAL_SET = 1
STOP_WORDS = {'to', 'i', 'you', 'a', 'the', 'u', 'and', 'is', 'in', 'my', 'for', 'your', 'of', 'me', 'have', 'call', 'on', 'are', 'that', 'it', '2', 'so', 'but', 'or', 'not', 'at', 'ur', 'can', 'if', 'with', 'will', "i'm", 'be', 'get', 'just', 'do', 'we', 'this', 'when', 'from', '&lt;#&gt;', 'go', 'up', 'all', 'no', '4', 'how', 'what', 'now', '.', 'like', 'got', 'know', 'was', 'free', 'out', 'come', 'am', 'its', 'then', 'good', 'send', '?', 'only', 'want', 'he', 'as', 'text', 'time', "i'll", 'by', 'love', '...', 'going', 'ok', 'ü', 'need', 'about', 'r', 'still', 'one', 'txt', 'n', 'see', 'our', 'dont', "don't", 'new', 'there', 'tell', 'she', 'been', 'any', 'think', 'reply', 'they', 'mobile', 'take', 'back', 'stop', 'some', 'please', 'has', 'did', 'home', 'an', '&', 'day', 'who', 'claim', 'her', 'hope', 'hi', 'had', 'make', 'give', 'pls', 'more', 'where', 'me.', 'd', 'phone', "it's", 'should', 'later', 'now.', 'much', 'him', 'happy', '-', 'great', 'sorry', 'after', 'ask', '&amp;', 'dear', 'you.', 'hey', 'da', 'say', 'well', 'e', 'really', 'im', 'here', 'last', 'way', 'very', 'meet', 'why', 'now!', 'night', 'miss', 'would', 'cos', 'c', 'too', 'today', 'oh', 'every', 'find', 'week', 'let', 'pick', 'them', 'number', 'win', 'work', 'contact', 'lor.', 'doing', 'nokia', 'said', 'right', "i've", 'cash', 'sent', 'keep', 'won', '1', 'cant', 'even', 'b', 'yeah', 'wat', 'thanks', 'also', 'message', 'were', 'went', 'next', 'his', 'anything', 'could', 'which', 'lol', 'feel', 'buy', 'gud', 'many', 'prize', 'gonna', 'tomorrow', ':)', 'it.', 'sure', 'msg', "can't", 'someone', 'per', "that's", 'lor...', '!', 'before', 'dun', 'always', 'us', 'sorry,', 'around', 'yes', 'wait', 'told', 'wan', 'over', 'service', 'something', '3', 'waiting', "you're", 'first', 'leave', 'customer', 'chat', 'care', 'other', 'already', 'down', 'thk', 'ok.', 'day.', 'getting', 'life', 'try', 'off', 'thing', 'may', 'place', 'being', 'morning', 'never', 'u.', 'trying', 'things', 'coming', 'nice', 'wish', 'you!', 'urgent!', "didn't", 'thought', 'draw', 'money', 'people', 'few', 'having', 'talk', 'use', 'x', 'k', 'late', 'ill', 'bit', 'babe', 'same', 'holiday', 'tone', 'finish', 'no.', 'thats', 'ya', 'friends', 'live', 'half', 'awarded', 'y', 'box', 'than', 'sleep', 'receive', 'latest', 'v', 'best', 'wanna', 'name', 'friend', '*', 'long', 'account', 'because', 'da.', '1st', 'you,', 'another', 'po', 'better', 'shows', 'jus', 'dat', 'meeting', 'mins', 'watching', 'smile', 'guess', 'into', 'might', 'quite', 'soon', 'stuff', 'wont', 'help', 'eat', 'car', 'sms', 'special', 'check', 'there.', 'real', '£1000', 'guys', 'ready', 'lunch', 'end', 'year', 'again', 'big', 'called', 'chance', 'enjoy', 'heart', 'speak', ',', 'man', 'play', 'home.', 'once', 'yup', 'between', 'ok...', 'person', 'made', '5', 'actually', 'probably', 'does', 'look', '2nd', 'maybe', '150ppm', 'reach', 'watch', 'video', 'ever', 'remember', 'pay', 'you?', 'done', "how's", '+', "he's", 'dis', 'hear', 'looking', 'guaranteed', 'little', 'didnt', 'two', 'put', 'den', 'start', 'shall', 'camera', 'cost', "there's", 'most', 'tonight', 'now?', 'luv', 'without', 'i.ll', 'time.', 'shit', 'dunno', 'minutes', 'mind', 'days', 'until', 'wif', 'selected', 'today.', 'thank', 'wanted', 'part', 'class', '16', 'forgot', 'nothing', 'says', 'lot', 'those', 'collect', 'hour', 'entry', 'goes', 'left', 'sweet', 'since', 'came', 'must', 'bt', 'job', 'able', 'hav', 'shopping', 'bring', 'god', 'bad', 'dad', 'early', 'network', 'room', 'means', 'abt', 'u?', 'juz', 'join', 'asked', 'yo', 'fuck', 'plus', 'world', 'xxx', 'dinner', 'till', 'ringtone', 'it,', 'later.', 'birthday', '4*', 'do.', 'tv', 'haha', 'face', 'everything', 'wake', 'line', 'orange', 'tones', 'fun', 'valid', 'bus', 'that.', 'saw', 'wen', 'making', 'out.', 'xmas', '&lt;decimal&gt;', 'important', '500', 'plan', 'wot', 'min', 'attempt', 'lor', 'makes', 'word', 'update', 'enough', '16+', "we're", "won't", 'tried', 'double', 'me?', "haven't", 'havent', 'show', 'top', 'haf', 'til', 'working', "what's", 'sexy', '18', 'missed', 'girl', 'plz', 'weekly', ':-)', 'guy', 'town', '£100', 'colour', 'price', 'school', 'todays', 'house', 'liao...', 'run', 'wid', 'texts', 'sat', 'stay', 'tot', 'details', 'wants', 'boy', 'yet', 'gift', '8007', 'set', 'free!', 'ard', 'delivery', 'pain', 'bonus', 'driving', '£2000', 'tonight?', 'missing', 'years', 'oh.', 'full', "we'll", 'change', '150p', 'g', 'either', 'these', 'while', 'saying', 'away', 'await', '6', 'pounds', 'work.', 'calls', 'hair', '£5000', 'guaranteed.', 'offer', 'hello', 'times', 'wil', 'coz', 'hot', '86688', 'hurt', 'babe,', 'yeah,', 'landline.', 't&cs', 'good.', 'lar...', 'final', 'forget', 're', 'took', 'month', 'finished', 'stop.', 'started', 'cause', 'mean', 'taking', 'both', 'happen', 'vouchers', 'music', '750', 'book', 'land', '£500', 'princess!', 'lose', 'shop', 'neva', 'feeling', 'drive', "she's", 'beautiful', 'apply', '£1.50', 'hours', 'no:', 'aft', 'now,', 'mob', 'urgent', 'test', 'old', '12hrs', 'expires', 'answer', 'each', 'believe', 'smoke', 'worth', 'gr8', 'tmr', 'found', 'aight', 'anyway', 'walk', 'up.', 'ring', 'baby', 'mail', 'right?', 'post', 'evening', 'busy', 'week.', 'head', 'line.', '7', 'thinking', 'bored', 'sch', 'family', 'knw', 'prize.', 'it?', 'dude', 'sad', 'goin', 'though', 'code', '100', 'pobox', 'date', 'decided', 'yourself', 'me...', 'trip', 'comes', 'too.', 'search', 'private!', 'statement', 'points.', 'identifier', 'me,', 'lots', 'leaving', 'today?', 'needs', 'sis', 'story', 'id', 'oso', 'sounds', 'thanx', 'angry', 'takes', 'unsubscribe', 'choose', 'food', 'lets', 'message.', 'calling', 'problem', 'mobileupd8', 'bed', 'office', 't', 'together', 's', 'o', 'hows', 'only.', 'words', 'fine', "doesn't", 'lucky', 'pa.', 'close', 'aight,', 'u!', 'sir,', 'open', '..', 'order', 'wit', 'noe', 'morning.', 'hold', '08000839402', 'bout', 'back.', 'tomorrow.', 'drink', 'dating', 'fucking', 'sae', 'visit', 'kind', '18+', 'pics', 'drop', 'fine.', 'collection.', ':-(', 'haha...', 'available', 'wkly', 'brother', 'wonderful', 'already?', 'alright', '08000930705', 'telling', 'class.', 'whole', 'second', 'girls', 'free.', 'ah?', 'wk', 'address', 'operator', 'code:', "you'll", 'services', 'yr', 'k,', 'their', 'fancy', "you've", 'carlos', 'log', 'weekend', 'easy', 'secret', 'thinks', 'true', 'anytime', 'card', 'sister', 'great.', 'touch', 'light', 'cool', 'messages', 'poly', '£250', 'question', 'ten', '10', 'u...', 'outside', 'pretty', 'voucher', 'b4', 'anyone', 'break', 'lovely', 'movie', 'de', 'online', 'lei...', 't&c', 'lesson', 'almost', 'used', '0800', 'prize!', 'else', 'gone', 'hit', 'felt', 'caller', 'landline', 'player', 'ni8', 'everyone', 'already.', 'night.', 'her.', 'awesome,', 'year.', 'darlin', 'finally', 'nite', 'meant', 'fr', 'congratulations', '87066', 'u,', 'dnt', 'unlimited', 'type', 'bslvyl', 'yes.', 'friendship', 'cool,', 'read', 'seeing', 'currently', 'talking', 'worry', 'couple', 'care.', 'eve', 'apply.', 'within', '2003', '800', 'kiss', 'it!', 'mum', 'opt', '10p', 'week!', 'rate', 'wife', 'ok?', 'party', '!!', 'mine', 'dear.', 'alone', 'w', 'gas', '||', 'wat...', "i'd", 'treat', 'national', 'smth', 'complimentary', 'cool.', 'here.', 'gotta', 'afternoon', 'sorry.', 'mom', 'direct', 'frnd', 'download', 'bank', 'well,', 'minute', 'leh...', 'know.', 'hard', 'company', 'case', 'then.', 'day,', 'blue', 'swing', 'award', 'th', 'supposed', 'month.', 'easy,', '2.', '4.', 'offers', 'un-redeemed', 'sea', 'yar', 'news', 'pub', 'weeks', 'game', 'mayb', 'gd', 'soon.', 'nt', 'picking', 'kiss*', 'least', 'pic', 'sex', 'enter', 'in.', 'smiling', 'it...', 'valued', 'eh', 'eg', 'ha', 'charged', 'crave', 'gets', '@', 'pass', 'yours.', 'checking', 'cut', 'loads', 'hi.', 'prob', 'yet.', "isn't", 'entered', 'askd', 'invited', 'winner', 'numbers', 'award.', 'dogging', 'txting', 'age', 'whats', 'wine', 'one.', 'love.', 'way.', 'ya,', 'muz', 'sleeping', 'march', 'txt:', 'tel', 'okay.', 'wana', 'club', 'fone', 'somebody', '1.', 'problem.', 'reading', 'via', 'jay', 'here,', 'st', 'discount', 'seen', 'phones', 'call.', 'asking', 'sending', '3.', '8', '£2,000', 'listen', 'through', 'darren', '£350', 'sun', 'whatever', '…', 'extra', 'yesterday', 'collection', 'whenever', 'sort', 'knew', 'already...', 'feels', 'it..', 'heard', 'crazy', 'frm', 'don', 'yes,', 'support', 'surprise', '*grins*', 'wrong', 'ok,', 'life.', 'loved', '9', 'auction', "wasn't", 'number.', 'this.', 'okie', 'comp', 'callertune', 'press', 'mobiles', 'knows', '=', 'out!', 'lar', 'rply', 'xx', 'now...', 'night?', 'representative', 'gave', 'computer', 'pa', "''", 'uncle', 'match', 'rates', 'mu', 'del', 'msgs', 'tired', 'doing?', 'spend', 'tomo', 'boytoy', 'orchard', 'kate', 'college', 'well.', 'yours', 'no,', 'sleep.', 'leaves', 'hmv', 'thanx...', 'far', 'figure', 'woke', 'me..', 'reason', 'mm', 'pm', 'point', 'booked', 'help.', 'cum', 'wat.', 'near', 'mobile!', 'hoping', 'across', ':', 's.', 'fine,', 'ts&cs', 'fantastic', 'fri', 'email', 'wishing', 'wonder', 'lost', 'ugh', 'sir.', 'charge', 'camcorder', 'poor', 'min.', 'otherwise', 'ntt', 'project', 'truth', 'happened', 'loving', 'thanks.', 'she.s', 'dreams', 'write', 'parents', 'empty', 'cup', 'copy', 'word:', 'myself', 'hungry', 'catch', 'uk', 'abiola', 'great!', 'reached', 'song', 'frnds', 'save', 'hee...', 'tickets', 'okay', 'up?', 'said,', 'specially', 'friday', 'that,', 'quiz', 'lovable', 'dream', 'hello,', 'safe', 'completely', 'mr', 'bath', 'staying', 'doesnt', 'money.', 'trust', 'using', 'ive', 'exam', 'lar.', 'bcoz', 'street', 'cd', 'disturb', 'yet?', 'stupid', 'unless', 'somewhere', 'accept', '£200', 'normal', ':(', 'merry', 'but,', 'small', 'txts', 'there,', 'brings', 'sir', 'huh', 'days.', 'ass', 'starts', 'there?', 'remove', 'terms', 'less', '£150', 'cs', 'can...', 'em', 'i.', 'm.', 'train', 'area', '–', 'day!', 'seems', 'sell', 'rite...', 'summer', 'store', 'today!', 'www.getzed.co.uk', 'gettin', 'tampa', 'want.', 'm', 'against', '£800', 'comin', 'convey', 'information', 'drugs', 'nobody', 'tht', 'congrats', 'doin', 'thinkin', 'flag', '12', 'entitled', 'info', 'link', 'quick', 'confirm', "you'd", 'weekend.', 'sms.', 'congrats!', 'nice.', 'k.', 'spent', 'loves', 'planning', 'coffee', 'ave', 'men', 'wishes', 'know!', 'boss', 'lunch.', 'ending', 'friend.', 'stop?', 'goto', 'later?', 'especially', "where's", 'freephone', 'bathe', 'however', 'mrng', 'yo,', 'bill', 'course', 'to.', 'side', 'kick', 'admirer', 'u-find', 'r*reveal', 'special-call', 'laptop', 'late.', 'lemme', 'own', 'content', 'charge.', 'usf', 'ends', 'rose', 'u..', 'haha,', 'christmas', 'plans', 'valentines', 'wiv', 'met', 'hg/suite342/2lands', 'you...', 'reference', 'bluetooth', 'rental', 'mrt', 'giving', 'din', 'kinda', 'is,', 'baby!', 'park', 'simple', 'him.', 'slow', 'afternoon,', 'self', 'cheap', 'nope', '150', 'kids', 'day?', 'tho', 'pound', 'noon', 'friends.', 'wish.', 'starting', 'again!', 'study', 'xy', 'ans', 'again.', 'home...', 'add', 'tc', 'glad', 'snow', 'omg', 'house.', 'no1', 'understand', 'possible', 'games', 'registered', 'medical', 'decide', 'love,', 'il', 'de.', 'miracle', 'good,', 'during', 'happiness', 'digital', 'place.', 'phone.', 'awaiting', 'film', 'chennai', 'tmr?', 'picked', 'mode', 'others', 'oh...', 'wow', 'ltd,', 'oredi...', 'mind.', 'tomorrow,', 'oops', 'wondering', 'difficult', 'south', 'john', 'simple..', 'hi,', "joy's", 'babe.', 'sitting', 'wat?', '"', 'them.', 'nah', 'request', '£900', '11', 'months', 'promise', 'click', 'wap', 'england', '87077', 'mark', 'sick', 'that!', 'replying', 'learn', 'saturday', 'kept', 'liked', 'ice', 'correct', 'etc', 'wun', 'following', 'stand', 'trouble', 'rain', 'hurts', 'password', 'cuz', 'weekends', 'special.', 'paying', 'anything.', 'room.', 'sunshine', 'sony', 'dvd', "uk's", 'lazy', 'back?', 'pray', 'sometimes', 'become', '62468', 'not,', 'hop', '$', 'need.', 'towards', 'net', 'slept', 'past', 'leh.', 'battery', 'showing', 'deep', 'lover', 'same.', 'definitely', 'night,', 'life,', 'sim', 'die', ':v', 'imagine', 'games,', 'buying', 'rest', 'kb', 'pete', 'immediately', 'fixed', 'access', '150p/msg', 'hand', 'yesterday.', 'urself', 'weed', 'ex', 'cash-balance', 'maximize', 'cash-in', '150p/msg.', 'sure,', 'ah...', 'motorola', 'so.', 'going?', 'rock', 'none', 'week?', 'too...', '3030.', 'loan', 'thru', 'style', 'tenerife', '6.', 'credit', 'rent', 'opinion', 'silent', '7.', 'phone,', 'ipod', 'mp3', "today's", '85023', 'savamob,', 'member', '£3.00', 'rather', 'hurry', 'up,', 'workin', 'gym', 'custcare', 'imma', 'valentine', 'alex', 'pc', 'sound', 'much.', 'under', 'king', 'looks', 'sit', 'library', 'wk.', "they're", 'lol!', 'tonight.', 'space', 'ago', '&lt;time&gt;', '36504', 'ones', 'charity', 'mate', 'mid', 'short', '08712460324', ':/', 'photo', 'earlier', '3g', 'ü...', 'mates', 'questions', 'bak', 'move', 'onto', 'cancel', 'complete', 'bb', 'shd', 'lor,', 'longer', 'vl', 'reaching', '20p', '1327', 'croydon', 'cr9', '5wb', 'welcome', 'msg:', 'players', 'fast', 'fact', 'hey,', 'morning,', 'moment', 'arrive', 'inside', 'holding', 'eyes', 'excuse', 'costa', 'sol', 'huh?', "who's", "wat's", 'not.', 'pls.', "god's", 'murdered', 'doing.', 'happens', 'cine', 'freemsg', 'hl', 'there!', 'yup...', 'again...', 'texting', 'ahead', 'sure.', 'usually', 'fyi', 'pleased', 'something?', 'job.', 'done.', 'bed.', 'don‘t', 'afternoon.', 'simply', 'shower', 'umma', 'birthday.', 'people.', 'worry.', 'eatin', '08712300220', 'standard', 'in?', 'inviting', 'turns', 'spoke', 'experience.', 'joined', 'deal', 'personal', 'persons', 'balance', 'rs', 'goodmorning', 'here?', 'say,', "u've", 'kallis', 'tncs', 'stuff.', 'mins?', 'horny', 'dint', 'sunny', 'worries', 'okie...', 'usual', 'power', 'only!', 'sign', 'track', 'return', 'round', 'msg.', 'posted', 'forward', 'motorola,', 'willing', 'order,', 'mistake', 'putting', 'al', 'man,', 'fullonsms.com', 'dear..', 'lift', 'wnt', 'vry', 'ldn', 'askin', 'tough', 'group', '"hey', 'best.', 'isnt', 'different', "t&c's", 'notice', 'award!', 'princess?', 'weekend?', 'depends', 'true.', '5.', '9.', '40gb', 'way,', 'children', 'while.', 'hotel', 'omw', 'warm', 'barely', 'daddy', 'spree', '!!!', '25p', 'vodafone', 'matches', "'", 'how?', '20', "u're", 'bedroom', 'lect', 'anyway.', 'torch', 'hey.', 'gap', 'wer', 'aftr', 'running', 'monday', 'wats', 'plan?', 'savamob', 'w45wq', 'norm150p/tone', 'future', 'bid', 'babe!', 'hmm', 'surely', 'fall', 'service.', 'yrs', 'user', 'murder', 'due', 'teach', 'worried', 'reply.', 'gay', 'iam', 'wherever', 'recently', '"our', 'it.."', "u'll", 'out,', 'nyt', 'holla', 'f', 'na.', 'fight', 'sipix', 'camera!', 'black', 'aiyah', 'http://www.urawinner.com', 'howz', "let's", 'luck!', 'not?', 'around?', '2day', 'over?', 'cell', 'lor..', 'dog', 'frens', 'is.', 'super', 'marry', 'yahoo', '08707509020', 'person,', 'share', '"i', '4th', 'nature', 'keeping', 'name.', '0870', 'except', '86021', 'single', 'then...', 'tomorrow?', 'london', 'buzz', 'walking', 'lookin', 'father', 'lol.', 'slowly', 'thing.', 'created', 'exciting', 'text.', 'list', 'bt-national-rate', 'yep', 'rate)', '09050090044', 'toclaim.', 'sae,', 'pobox334,', 'stockport,', 'sk38xh,', 'cost£1.50/pm,', 'max10mins', 'awesome', 'said:', 'number,', 'movies', 'ahmad', 'thnk', 'freemsg:', 'semester', 'official', 'though.', 'sed', 'wife,', '.....', 'role', 'checked', 'tear', 'hell', 'added', 'budget', 'meds', 'bugis', 'darling', 'callers.', '*9', 'co', 'searching', 'sunday', 'naughty', 'i‘m', 'stock', 'eating', 'hello!', 'nigeria.', 'tyler', 'hospital.', 'weak', 'ride', 'red', 'cinema', 'situation', 'customer,', 'review', 'pain.', 'pleasure', '530', 'see.', 'changed', 'page', 'happened?', 'cabin', "b'day"}
CURRENCY_CHARACTERS = ['$', '€', '£', '¥', '₹', '₩', '₽', '₺', '฿', '₫', '₴', '₦', '₲', '₵', '₡', '₱', '₭', '₮', '₦', '₳', '₣', '₤', '₧', '₯']

# Read all the lines in SMSSpamCollection to a list
file_path = 'SMSSpamCollection'

with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

words = []
label = []
# Print the lines to verify
for line in lines:
    label.append(line.strip().split()[0])
    words.append(line.strip().split()[1:])

def replace_digits(word):
    return re.sub(r'\d{4,}', lambda x: '1' * len(x.group()), word)
words = [[replace_digits(word) for word in word_list] for word_list in words]

def replace_currency(word):
    for char in CURRENCY_CHARACTERS:
        word = word.replace(char, '$')
    return word
words = [[replace_currency(word) for word in word_list] for word_list in words]

def lowercase(word):
    return word.lower()
words = [[lowercase(word) for word in word_list] for word_list in words]

def remove_common(word):
    return word if word not in STOP_WORDS else ""
words = [[remove_common(word) for word in word_list] for word_list in words]



# Split the data into training and test sets
train = words[:int(len(words)*TRAINING_SET_RATIO*TOTAL_SET)]
test = words[int(len(words)*TRAINING_SET_RATIO*TOTAL_SET):int(len(words)*TOTAL_SET)]

# Identify the list of unique terms in the train set
unique_terms = set()
for tokens in train:
    unique_terms.update(tokens)

# Calculate the inverse document frequency (IDF) for each term in the train set
def calculate_idf(term, train_set):
    num_docs_with_term = sum(1 for doc in train_set if term in doc)
    return math.log(len(train_set) / (1 + num_docs_with_term))

idf = {term: calculate_idf(term, train) for term in unique_terms}

# Calculate the term frequency (TF) for each term in a document
def calculate_tf(term, document):
    return document.count(term) / len(document)

# Calculate the term frequency for each term in the train set
train_tf = []
for doc in train:
    doc_tf = {term: calculate_tf(term, doc) for term in doc}
    train_tf.append(doc_tf)

# Calculate the term frequency for each term in the test set
test_tf = []
for doc in test:
    doc_tf = {term: calculate_tf(term, doc) for term in doc}
    test_tf.append(doc_tf)

# Calculate the TF-IDF for each term in the
train_tfidf = []
for doc_tf in train_tf:
    doc_tfidf = {term: tf * idf[term] for term, tf in doc_tf.items()}
    train_tfidf.append(doc_tfidf)


def euclidean_distance(vec1, vec2): 
    total = 0
    for term in vec1:
        if term in vec2:
            total += (vec1[term] - vec2[term]) ** 2
    return math.sqrt(total)

def find_knn(k, test_set, train_tfidf):
    distances = dict()
    for i in range(len(train_tfidf)):
        distances.update({i: euclidean_distance(test_set, train_tfidf[i])})
    sorted_distances = sorted(distances.items(), key=lambda item: item[1], reverse=True)
    return sorted_distances[:k]

TEST_START_INDEX = int(len(words)*TRAINING_SET_RATIO*TOTAL_SET)

def categorize_knn(k, test_index, train_tfidf):
    knn = find_knn(k, test_tf[test_index], train_tfidf)
    total_spam = 0
    total_ham = 0
    for i in range(len(knn)):
        if (label[knn[i][0]] == 'spam' and knn[i][1] != 0):
            total_spam += 1
        elif (label[knn[i][0]] == 'ham' and knn[i][1] != 0):
            total_ham += 1 
    if (total_ham > total_spam):
        return "ham"
    return "spam"

k = 5

correct_spam = 0
correct_ham = 0
total_spam = 0
total_ham = 0
for i in range(0, len(lines)-TEST_START_INDEX):
    indexed_label = categorize_knn(k, i, train_tfidf)

    if (label[i+TEST_START_INDEX] == "spam"):
        if (indexed_label == "spam"):
            correct_spam += 1
        total_spam += 1
    elif (label[i+TEST_START_INDEX] == "ham"):
        if (indexed_label == "ham"):
            correct_ham += 1
        total_ham += 1
    else:
        "ERROR: Neither spam nor ham"

print("True Positives:", correct_spam)
print("False Positives:", total_ham - correct_ham)
print("True Negatives:", correct_ham)
print("False Negatives:", total_spam - correct_spam)

print("Accuracy:", (correct_spam + correct_ham) / (total_spam + total_ham))
print("Precision:", correct_spam / total_spam)
print("Recall:", correct_spam / (correct_spam + total_ham - correct_ham))
print("F1 Score:", 2 * (correct_spam / total_spam) * (correct_spam / (correct_spam + total_ham - correct_ham)) / ((correct_spam / total_spam) + (correct_spam / (correct_spam + total_ham - correct_ham))))
