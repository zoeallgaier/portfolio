// — Canvas (matches canvas.js) ———————————————————————————————————————————————
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const canvas = document.querySelector('.hero-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const GAP = 24;
  let W = 0, H = 0, cols = 0, rows = 0, t = 0, running = false;

  function resize() {
    W = canvas.offsetWidth;
    H = canvas.offsetHeight;
    if (!W || !H) return;
    const dpr = window.devicePixelRatio || 1;
    canvas.width  = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cols = Math.ceil(W / GAP) + 1;
    rows = Math.ceil(H / GAP) + 1;
    if (!running) { running = true; draw(); }
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const x = c * GAP;
        const y = r * GAP;
        const w1 = 0.5 + 0.5 * Math.sin(c * 0.22 + r * 0.14 - t * 0.7);
        const w2 = 0.5 + 0.5 * Math.sin(c * 0.11 - r * 0.18 - t * 0.43);
        const wave  = w1 * 0.6 + w2 * 0.4;
        const alpha = 0.02 + 0.40 * wave;
        const rad   = 0.55 + 0.45 * wave;
        ctx.beginPath();
        ctx.arc(x, y, rad, 0, Math.PI * 2);
        const dark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        ctx.fillStyle = dark
          ? `rgba(255,255,255,${(alpha * 1.3).toFixed(3)})`
          : `rgba(0,0,0,${alpha.toFixed(3)})`;
        ctx.fill();
      }
    }
    t += 0.011;
    requestAnimationFrame(draw);
  }

  new ResizeObserver(resize).observe(canvas.parentElement || document.body);
}());

// — Band names ———————————————————————————————————————————————————————————————
const NAMES = [
  "Moderately Albino",
  "Bag Of Bumholes",
  "Earball",
  "Terrible Couch",
  "Super Good Scoop",
  "Devil's Hole",
  "Plastic Existence",
  "21st Century: We Be Licking",
  "Waterproof Baby",
  "Wet Sweater",
  "Chicken Diarrhea",
  "In Search Of Reality",
  "Unequivocally Bussing",
  "Ronald McReagan",
  "Heal That Mouse!",
  "Pocket Full Of Celery",
  "Cleavage Cupcakes",
  "Violent Santa Giver",
  "Fat Milk",
  "Flapchulants",
  "The Witches Eye",
  "Brown Vs Board Of Education Vs Godzilla Vs Kong Vs Roe Vs Wade Vs Alien Vs Predator",
  "Meat Cloud",
  "Mutual Distraction",
  "Personal Snake Bias",
  "Uvula Amputation",
  "Grabbing Farts",
  "Heathen Ice Cream Spoon",
  "Cheesepuffs (The Best Animal)",
  "Gatekeeping Turds",
  "Memories Of The Future",
  "God's Military",
  "Full Body Skin Graft",
  "Churro Chopper",
  "Pinching The Loaf",
  "The Mall Sucks",
  "Our Spores Make Contact",
  "OCD Alchemy",
  "MILF Practice",
  "IBS Humidifier",
  "Gender Canyon",
  "Dog & Cat Grooming",
  "Buddha Princess",
  "5-Pin Bowling",
  "Strange Hemorrhoid Encounter",
  "Monkey Nest",
  "Third Wheeling A Family Reunion",
  "Red Ghonornea",
  "Deaf Applause",
  "Philosophical Buzzwords",
  "Grip Strength On Beast Mode",
  "Ginger Beef",
  "Tainted Window To The Soul",
  "Disaster Bisexuals",
  "Ghandi Was A Capricorn",
  "Insecure Stinkybutt",
  "Summer School Study Sesh",
  "Healthy Mental Illness",
  "The Second Coming (Out)",
  "Limit Larper",
  "Meat Candle",
  "Selectively Mute",
  "Blessed Homies",
  "Double Puppy Gassed",
  "Schizophrenic Orca",
  "Ini De Beninging",
  "San Antanio Scoreboard",
  "Soft Jam",
  "Excessive With The Fur",
  "ChatPCP",
  "Minecraft Arson",
  "Cockroaches Of The Flora",
  "Non-Derogatory Epoxied Garage",
  "Captured By The Essence",
  "Volcanizing Solution",
  "Shart Now Loading",
  "Stanford Friendship Experiment :)",
  "Enlightened By The Pastrami",
  "Epistemological Nightmare",
  "Digital Footprint Dance Break",
  "Sacrificial Pony",
  "Associated Drip",
  "Lore Implications",
  "Farmtime Land",
  "Barn On Fire",
  "Fresh Off The Counter",
  "Mormon Cosplay",
  "Magnus Opium",
  "Intentional Accident",
  "Explicit Respect, Implicit Disrespect",
  "Sacrificial Stallion",
  "B-Phex Triplet",
  "Tear Inducing Soup",
  "A Week And A Half Of Body Dysmorphia",
  "Satanic Panic",
  "Clifford The Red40 Dog",
  "Extreme Blessings",
  "Get Off The Pier!",
  "The Flaw",
  "Criminal Amount Of Ass",
  "King Obstructionist",
  "The Shiddler",
  "Poop Incarnate",
  "The Lord Hates Quitters",
  "Golden Goblin",
  "Corporate Operated Community",
  "Poop Attack (I Had No Choice)",
  "Broad Spectrum",
  "Rival Hairline",
  "Geriatric Rizz",
  "Natural Selection",
  "Thou Shalt Print",
  "Unintentional Invasion",
  "Well-Rounded Idiot",
  "Goblin Zoomies",
  "Kissed By Ares",
  "Partial Recall",
  "The Twerk",
  "Touching Warm",
  "Eat Your Kibble",
  "Kansas Ham-Eye",
  "Microdosing E-Coli",
  "Food Court",
  "Goat's Ego",
  "Where The Gays At?",
  "STD In A Chicken",
  "Community Cookie",
  "Slay Or Stupid",
  "Fully Torqued",
  "Horse Meat Disco",
  "Off The Planet By Minute 5",
  "Spiritual Scurry",
  "Jaundicey Lighting",
  "Rust Belt Legend",
  "Rapid Onset Jaundice",
  "Off Duty Telletubby",
  "Syphillis Tube",
  "Effortlessly Vile",
  "Bested By The Fumes",
  "Monkey Monday",
  "Lightweight Grandpa",
  "Memory Voicemails",
  "Mo'Thickah",
  "Malnourished Pimps",
  "Casual Divinity",
  "Bloodshot Diva",
  "Technically Amazing",
  "Poseidon's Kiss",
  "Intermission: Soup Time",
  "Unscheduled Pirating",
  "Cain Instinct",
  "Potential Beef",
  "Urban Foraging",
  "Red-40 Monologue",
  "Executive Command: Fortnite",
  "Being Goofy In The Corner",
  "Bunghole",
  "Offense Mechanism",
  "Kardashian Empire",
  "The Ultimate Loser",
  "I'm Just Existing",
  "Territorial Feud",
  "The Oppenheimer Special",
  "Corporate Brainrot",
  "Adjective Tough",
  "Piss Thyself",
  "Caffeine Sobriety",
  "Claw Enjoyer",
  "Basic Nonsense",
  "Oblique Perspectives",
  "Mud Breath",
  "Confined Scurry",
  "Doorknob Confessions",
  "A Touch Of Fraud",
  "Stylistic Perfection",
  "Proper Barf Sesh",
  "Hardcore Floor Enjoyer",
  "Famine Energy",
  "Obviously Commensurate",
  "Theoretical Decapitation",
  "No Water, Just Mud",
  "Celebrity Favoritism",
  "Currently Birthing",
  "Moist Dissociation Chamber",
  "Borrowed Valor",
  "White Collar Beef",
  "Impenetrable Bog",
  "Verbal Outburst",
  "Ancient Astronaut Theorists",
  "3-Sentence Headline",
  "Stinky, Sweaty, Slippery Monks",
  "Defrosted Rust",
  "Blood Transfusion Turtle",
  "Quintessential Pookie",
  "Unwavering Graditute",
  "Independence Day For Bigfoots",
  "Rockin' Sqautchin' Territory",
  "Impossibly Large",
  "Covfefe",
  "Violently Introduced",
  "Smile Checkpoint",
  "Essence Of Yeast",
  "Steel Ghonorrea",
  "Straight To The Grand Canyon",
  "Fecal Incident",
  "Glacial Pace",
  "Registered God Particle",
  "Jolly Implication",
  "Secret Sipper",
  "Androgynous Sloths",
  "Financial Hangover",
  "Stink Portal",
  "Tactile Smell",
  "Earthworm Mentality",
  "Hag Mode",
  "Homogenous Yogurt",
  "Trickle Down Gossip",
  "Sober Scurry",
  "Doomsday Glacier",
  "Superior Nerd",
  "Cracky Behavior",
  "Good Old Fashioned Pawn Shop Waffle-Iron Bidding War",
  "LoinFire",
  "Sad Beige Moms",
  "Giuseppe And The Overcooked Raviolis",
  "Tragically Hetero",
  "Malicious Intent",
  "Communal Clamp",
  "LinkedIn Rizz",
  "Lizard Receptors",
  "Secondably",
  "Hangry And Stuck In Traffic",
  "Kick And A Hi Hat",
  "Library Blood Pact",
  "Hypnotically Caucasian",
  "Monkeyface Prickleback",
  "June Sucker",
  "Throwing Off The Hump",
  "Mullet With Headlights",
  "Distribution Date Matrix",
  "Drunk Toes",
  "Pop Rap Rock Star",
  "Dangular Fidget",
  "Princess Passenger",
  "The Harvested",
  "Yours Whimsically",
  "Stethoscope Symphonies",
  "Cinematic Dookie",
  "Holy Adultery",
  "Corruptions Of Form",
  "Simultaneous Sniff",
  "Clurb Stomp",
  "Shart Party",
  "Operation Dude Brigade",
  "Flolling Rinlula",
  "Almost A Pear",
  "Daft Sod",
  "Daft Mainstream",
  "Whispers In The Wind",
  "The Unusual Suspects",
  "Poot",
  "El Cangrejo Submission",
  "A Lifetime Of Free Colonoscopies",
  "Heterophobia",
  "Beehives Are Nature Grenades",
  "Well-Mannered Riot",
  "Black Tar Red40",
  "Calcified Pineal Gland",
  "Ultimate Stank Face",
  "Pathologically Incurious",
  "This Week's Doily",
  "Reasonably Chill",
  "Lard Carcass",
  "Demurely Early",
  "The Entire State Building",
  "Times New Roman Firing Squad",
  "Mental Shadow Boxing",
  "In A Euphemistic Way",
  "Concepts Of A Band",
  "Please Excuse My Dark Ambient Swag",
  "Italian Paper Mache",
  "Couple's Descent",
  "Blue-Tinted Vibe",
  "Geometric Visual Albedo",
  "Naked & Boring",
  "Karmic Heads",
  "Heterosexual Flamboyance",
  "Wild But Desensitized",
  "Alopecia Eyebrows",
  "Fart In A Shoebox",
  "Wet Cheese",
  "Booger Whistle",
  "Assorted Miscreants",
  "Godzilla Multiball",
  "Positive Blame",
  "Stellar Aftercare",
  "Saltwater Blockade",
  "Muskration Lore",
  "Nebraska Split",
  "Particularly Atrocious",
  "Lasagna Hog",
  "Raw Dudery",
  "Algorithmic Slay",
  "Concepts Of Thoughts & Prayers",
  "Denial Against The Machine",
  "Chronically Alive",
  "Conquered By Adderal",
  "Icky Caca Pitch",
  "Drones Over New Jersey",
  "A Pickle And A Half",
  "Just The Right Amount Of Couch",
  "Chickpea Fest",
  "Surge Pricing For Geese",
  "Panic Decorating",
  "Spiritual Harrassment",
  "Earwax Vape",
  "Mutual Rotting",
  "Stacking Up The Beanstalk",
  "Chemical Afterburn",
  "Clurb Mindset",
  "Trailer Park Barbie",
  "Sanest Conspirator",
  "Peer Reviewed Lane Change",
  "ChefferPoo",
  "Divas In The Alley",
  "Dark Web Botox",
  "Combined Slay",
  "Old Fart Freeway",
  "Bastard Pastry",
  "Asymmetrical Buttcrack",
  "Subtle Goblin",
  "Loser Emporium",
  "Trojan Compliment",
  "Freud And The Eels",
  "Gen Alpha Gentrification",
  "Clark & Shadow",
  "Robloxably Compatible",
  "Prehistoric Haberdashery",
  "Nature's Botox",
  "Domestic Bliss",
  "Wet Crumbs",
  "Semironically",
  "Ambient Sweat",
  "Feetwalkers",
  "Sleeve Of A Mouse",
  "Undulated Yolk",
  "Mutual Shart",
  "Embrace The Poot",
  "Baddie Gathering",
  "Irrational Boob",
  "Offset Salmonella",
  "Scheduled Booty Shaking",
  "Breast Augmentation Season",
  "Avodaco",
  "Baby Onion Freak Person",
  "Was It Bald?",
  "Chad Therizinosaurus",
  "Band Name",
  "Spoiled Chicken In The Spanish Pavilion",
  "Cocktail Couture",
  "League Of Absence",
  "Rot Essence",
  "48 Duraflame Logs",
  "An Honest Punch In The Face",
  "Mystery Assets",
  "Turkey Middle Soup",
  "Pretty Lady Called Me Pretty",
  "Just A Little Pat Pat",
  "Trace Elements Of Connection",
  "Snuffleuffugus",
  "Italicized Ish",
  "Cyborg Ass",
  "Pretty Much Post Mortem",
  "Threat Of Giggling",
  "Skalter White Yo",
  "I'll Think Of Something",
  "Fluffbutt",
  "Death by Pride",
  "Rabies Denial",
  "Squirrel Overdose",
];

// — Generation ———————————————————————————————————————————————————————————————
function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

let queue    = shuffle(NAMES);
let queueIdx = 0;
let history  = [];
let histIdx  = -1;

function advance() {
  if (histIdx < history.length - 1) {
    histIdx++;
    return history[histIdx];
  }
  if (queueIdx >= queue.length) {
    const last = queue[queue.length - 1];
    queue = shuffle(NAMES);
    if (queue[0] === last) {
      const swap = 1 + Math.floor(Math.random() * (queue.length - 1));
      [queue[0], queue[swap]] = [queue[swap], queue[0]];
    }
    queueIdx = 0;
  }
  const name = queue[queueIdx++];
  history.push(name);
  histIdx = history.length - 1;
  return name;
}

function retreat() {
  if (histIdx <= 0) return null;
  histIdx--;
  return history[histIdx];
}

// — DOM ——————————————————————————————————————————————————————————————————————
const nameEl    = document.getElementById('bandName');
const counterEl = document.getElementById('counter');
const btn       = document.getElementById('generateBtn');
const prevBtn   = document.getElementById('prevBtn');
const nextBtn   = document.getElementById('nextBtn');

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

let buildTimer = null;

function buildChars(name, direction) {
  clearTimeout(buildTimer);
  buildTimer = null;

  const isBack   = direction === 'back';
  const exitAnim = isBack ? 'charExitBack' : 'charExit';
  const existing = nameEl.querySelectorAll('.char');
  let exitDelay  = 0;

  // Animate existing chars out
  if (existing.length && !reducedMotion) {
    const exitGap = Math.min(0.018, 0.25 / existing.length);
    const exitDur = 0.28;
    existing.forEach((ch, i) => {
      const d = i * exitGap;
      ch.style.animation = `${exitAnim} ${exitDur}s cubic-bezier(0.55,0,1,1) ${d.toFixed(3)}s both`;
      exitDelay = Math.max(exitDelay, d + exitDur);
    });
  }

  const buildNew = () => {
    buildTimer = null;
    nameEl.innerHTML = '';
    nameEl.classList.toggle('going-back', isBack);

    if (reducedMotion) {
      nameEl.textContent = name;
      return;
    }

    // Scale enter gap: total 0.5s–1.5s regardless of name length
    const totalTime = Math.max(0.5, Math.min(1.5, name.length * 0.026));
    const gap = totalTime / name.length;
    let charIdx = 0;

    // Wrap each word so the browser only breaks at spaces, not mid-word
    name.split(' ').forEach((word, wi, arr) => {
      const wordSpan = document.createElement('span');
      wordSpan.className = 'word';

      [...word].forEach(ch => {
        const mask  = document.createElement('span');
        mask.className = 'char-mask';
        const inner = document.createElement('span');
        inner.className = 'char';
        inner.textContent = ch;
        inner.style.animationDelay = `${(charIdx * gap).toFixed(3)}s`;
        mask.appendChild(inner);
        wordSpan.appendChild(mask);
        charIdx++;
      });

      nameEl.appendChild(wordSpan);
      if (wi < arr.length - 1) {
        nameEl.appendChild(document.createTextNode(' '));
        charIdx++; // keep timing aligned with space
      }
    });
  };

  if (exitDelay > 0) {
    buildTimer = setTimeout(buildNew, Math.ceil(exitDelay * 1000));
  } else {
    buildNew();
  }
}

function updatePrevBtn() {
  prevBtn.disabled = histIdx <= 0;
}

function showName(direction = 'forward') {
  const name = direction === 'back' ? retreat() : advance();
  if (!name) return;

  buildChars(name, direction);

  counterEl.textContent = `${histIdx + 1} of ${NAMES.length}`;

  updatePrevBtn();
}

btn.addEventListener('click',     (e) => { e.stopPropagation(); showName('forward'); });
nextBtn.addEventListener('click', (e) => { e.stopPropagation(); showName('forward'); });
prevBtn.addEventListener('click', (e) => { e.stopPropagation(); showName('back'); });

document.querySelector('.hero').addEventListener('click', () => showName('forward'));

document.addEventListener('keydown', (e) => {
  if (e.target !== document.body) return;
  if (e.code === 'Space' || e.code === 'ArrowRight') {
    e.preventDefault();
    showName('forward');
  } else if (e.code === 'ArrowLeft') {
    e.preventDefault();
    showName('back');
  }
});

showName('forward');
