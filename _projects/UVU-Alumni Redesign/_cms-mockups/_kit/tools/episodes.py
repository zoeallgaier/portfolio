"""Forever Wolverines Podcast episodes, newest first (from the Spotify show page, Oct. 2026).
(id, guest, tagline, date, minutes, host, image hash suffix)"""
IMG = 'https://i.scdn.co/image/ab6772ab000030ae'
SHOW = 'https://open.spotify.com/show/0jjnDHtCAWyyTIzDSZYxHp'
EP = [
    ('4aORjvhnM070uKeWZNUjMt', 'Krystal Gates ’23', 'Welcome the Unexpected Through Internships', 'Oct. 13, 2026', 29, 'Ike', '35c0bd5bcfc91a07732ef3c9'),
    ('1rsNiCcRbFivhbQTnD3UQa', 'Kelsie Call ’22', 'Use Your Voice, Influence Change', 'Sept. 29, 2026', 39, 'Nate', '42ef4d12ec8b0721c031b4f8'),
    ('1o9pV8sohXYI7Cu7tXjSoY', 'Michaela King ’22', 'Care About the Details, Find Your Fit', 'Sept. 15, 2026', 32, 'Shelby', '4bf176f213f5fd6f1ad76a36'),
    ('6aRdqjXn2HDwGGFw8pnKa7', 'Linda Pomar ’21, CMHC ’23', 'Relax and Embrace Imperfection', 'June 2, 2026', 31, 'Brooke', 'bdbed68a637a6919f7a7382c'),
    ('5sj2M1DgFRSsXfcJ4T4WA7', 'Kevin “DoK” Woods ’12', 'Reinvent Yourself, Transform Your World', 'May 26, 2026', 46, 'Mohamed', '1622bd657a3dcfd6554500c4'),
    ('2nMKRzXtzVJFSz6R9R3YbD', 'Megan Weaver Hillier ’21', 'Advocate Often and Put People First', 'May 12, 2026', 31, 'Shelby', '764438892f9e29d45e4c6ae2'),
    ('6FDcQRQj0KqKrndXplBTGv', 'Lacey Cherrington ’98', 'Regret Nothing and Be Intentional', 'May 5, 2026', 40, 'Nate', '8dcbe1e1439e3b9e69aac57d'),
    ('2qSFEQ77WuYqaLtXhVVJWS', 'Salifou Fofana ’17, MBA ’19', 'Plan but Know It’s Never Too Late', 'April 28, 2026', 42, 'Mohamed', '46bca0f2c66d27a294f44d9d'),
    ('3E6WEugZCdjokAfEC3mhet', 'Matt Bryson ’17', 'Build Your Future Through Situations of Opportunity', 'April 21, 2026', 43, 'Mohamed', '692c453ba053117ef639533e'),
    ('29ZvYgmTSIUsAsiqckX3RV', 'Amanda Kimball ’11, M.Ed. ’21', 'Show Up and Trust Yourself', 'March 17, 2026', 50, 'Brooke', 'd0833ef2847556b419df8118'),
    ('0ZUDDboG1NkhZR7IWmEN4L', 'Myrna June Rodriguez Whittington ’16', 'Know You Belong While Failing Fast', 'Feb. 24, 2026', 34, 'Larissa', 'c8660f81606cfc497feb8ab8'),
    ('2HOWhqlJtQc8aqFDhzrloi', 'Kelly Henderson ’20', 'Stress Less, Connect More', 'Feb. 10, 2026', 32, 'Nate', 'e460b3d154cdf3d7497bbd7c'),
    ('5IV9hNqb2Lxobdxirx6xm1', 'Oumar Traore ’22', 'Learn, Grow, and Give Back', 'Jan. 27, 2026', 31, 'Mohamed', 'daf2eddb7ee0d30a34901c1f'),
    ('0f67ZaocvMYT0tEhNhC5Qd', 'Maddie Heywood ’20', 'Adapt With the Chaos to Unlock Your Potential', 'Jan. 13, 2026', 35, 'Shelby', '46374cee1bc61824df7047ad'),
    ('0nlca5gixn3XcyKEgSAw3p', 'Meet the Student Alumni Ambassadors', '2025–26', 'Dec. 3, 2025', 4, None, '6d02b9262425577c4d2c6f0d'),
    ('3N5n2c0XxHwooqCGKgGclM', 'Kara North ’07', 'Evolve Your Success One Goal at a Time', 'Sept. 2, 2025', 35, 'Kaleah', '50e24fa253f20e5767dbca7c'),
    ('4njFxdt5Rd3JV12TgMAL2K', 'Emilee Henriquez ’19', 'Live Your Truth by Making Choices for Who You Are Today', 'Aug. 12, 2025', 43, 'Savannah', 'b90423e482eebd6bb639ec54'),
    ('4dKUYtY1giD5i6LvMcrBxn', 'David Dekker ’18', 'Change Gracefully, Learn Always, and Embrace the Unknown', 'July 15, 2025', 25, 'Vagner', '8b1b5a5e4cc65f430f66c8bc'),
    ('5uXbpwNLTq54IWjqHTAKNk', 'Brandon Davies ’15', 'Ask the “Stupid” Questions and Be True to Yourself', 'July 1, 2025', 50, 'Callie', '4b2dd176e4c2ece4d36e7931'),
    ('5CQIyIpEmgcZ20WE6mIG9p', 'Colton Simons ’16', 'Allow Life to Unfold by Practicing Patience', 'June 17, 2025', 42, 'Brooke', 'c111c1bb7cb4c4422504db7c'),
    ('7nN2EvYmcYiEevNBVUuOKA', 'Wendy Wright ’17', 'Prepare for Your Future by Collaborating With Confidence', 'May 27, 2025', 44, 'Mandy and Savannah', '8e70c72766e7d87eb26be767'),
    ('042snCqgXKqpbAtYLbaFDI', 'Bakary Camara ’15, MBA ’17', 'Mitigate Risk in Your Career by Nurturing Relationships', 'May 6, 2025', 44, 'Mohamed', '2a647ea6236170727741ade5'),
    ('0UhsbA4wv37T706Rc7v4PQ', 'Andre Jones ’18', 'Champion Your Strengths Through Leadership Opportunity', 'April 22, 2025', 34, 'Mohamed', '91673b7d5574950555db1b6f'),
    ('7BAK7S999HNe28Kwftfhnj', 'Melanie Wolfe ’22, MSW ’24', 'Tackle Your Fear by Relying on Resources', 'April 8, 2025', 30, 'Savannah', '65092fc0a92b988f17ddcaed'),
    ('3LUAXBTDCxsR142TmiwBda', 'Kim Hopkins ’21', 'Embrace Growth in an Ever-Changing Industry', 'March 18, 2025', 36, 'Kaleah', '054901b550c858aad29ac324'),
    ('7C29sOSn5N0DfUQ9arnHtu', 'Megan Johnson ’08', 'Influence Your Community Through the Ability to Listen', 'March 4, 2025', 50, 'Mandy and Savannah', 'de8f278feb4c88cadcef448b'),
    ('6CtORE8AB51NA9IxXxujNx', 'Chelsea Gipson ’18', 'Excel Through Opportunity by Finding Your Niche', 'Feb. 25, 2025', 36, 'Callie', 'f09c2f153afc737158f6b71d'),
    ('1kjN9i0PUqF3QWDwwJqPuO', 'Tiana Wynn ’24', 'Discover Your Passion and Allow It to Lead You', 'Feb. 11, 2025', 30, 'Mohamed', 'd2aed177f527bb4cc1f1cd4f'),
    ('4teOEPsiCkX18GJjoo3tA2', 'Meet the Student Alumni Ambassadors', '2024–25', 'Jan. 24, 2025', 3, None, '23cd4be10365cb1f8cbe29ff'),
    ('6d8GIf4prozfOqbwTgl2f4', 'JC Arauz ’21', 'Create Connection Through Confident Communication', 'Jan. 22, 2025', 36, 'Vagner', '7e9385cfaac7deaa82d99a7a'),
    ('5InPl398yQIjSDF19aHupA', 'Linda Makin ’02', 'Leave a Legacy by Believing in Yourself', 'Jan. 6, 2025', 41, 'Brooke', '4e7edb2690e588d9415b5cf4'),
]


def latest_feature(variant='hatch'):
    """Latest episode as a linked photo (people, not the show logo) + caption. Replaces the Spotify show embed,
    whose player shows the show artwork (the logo)."""
    i, guest, tag, date, mins, host, h = EP[0]
    url = f'https://open.spotify.com/episode/{i}'
    hl = f' · Hosted by {host}' if host else ''
    return f'''<figure class="al-media al-media--{variant} al-media--wide al-media--episode">
                  <a href="{url}" target="_blank" rel="noopener"><img src="{IMG}{h}" data-cms-src="/alumni/connect/images/podcast/{i}.jpg" alt="{guest} on the Forever Wolverines Podcast set" width="1280" height="719"><span class="al-play" aria-hidden="true"></span><span class="sr-only-al">Listen to {guest} on Spotify (opens in a new tab)</span></a>
                  <figcaption><span class="al-card-tag-text">Latest Episode · {date} · {mins} min</span><strong>{guest}</strong> {tag}{hl}</figcaption>
               </figure>'''
