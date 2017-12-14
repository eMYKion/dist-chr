# Requirements
1. python3
2. nltk
3. wordnet (via nltk)
4. autocomplete

# Readings:

1. Plutchik's wheel of emotions
2. Peter Norvig Spell Check
3. Wu-Palmer Similarity

# Game Flow: 

(from command-line )

1. talk to people (picture window)
  a. user types
    i. to make a decisions from a set of options
    ii. to start out conversation and set topic (if the user started conversation)
  b. user views preset text - yours (based on decision) and person's
  c. you can lose and gain items
  d. time will pass quickly
		
2. trvl to places
  a. time will pass quickly based on effective distance to place
		
3. idle (at command-line)
  a. time will pass slowly (changes by real time)
  b. NPC may initiate conversation with you (they will set topic) [see 1.]
  c. user can pass time quickly (./pass)

# Dialogue Model
1. `[player1]` says `[phrase1]`
2. `[player2]` responds
  a. `[player2]` adds `[topic1]` from `[phrase1]` to `[thoughts]`
  b. `[player2]` `[emotion]` is calculated from `[thoughts]`
  c. `[player2]` constructs `[phrase2]` from `[script]` with `[topic1]`
  i. `[phrase2]` is a function of mood (see section: Script Model).

# Recursive Script Model

1. a fixed script with word-functions (based on python .format()), everything accessed from the `gbl` (global) dictionary:
  a. `slc` (selectors) - based on mood (choose max of inner product of current emotion and requirement, and include it in the text)
  b. `opt` (optionals) - based on mood (if cosine from inner product of emotion and requirement is higher than THRESHOLD, then include it in the text)
  c. `chr` (characters) - ANY public character attribute taken from runtime
    i. data fields characterized by character file (see section: Characters)
    ii. organized by character proper name, player name is _player
  d. ALL subvalues will be returned with their `.format()`-ed versions, so even child phrases can have name substitutions, etc.
  e. pretty much all strings are `.format()`-ed

2. all ACTION statements are accessed from the `act` (action) dictionary
  
3. XML syntax:

TODO:: select from list any of whose options satisfy mood, or random

script.xml
```xml
<script npc_name="Mary Jane">
  <p spkr="Mary Jane">{gbl.slc[greetings]}<p><!--this format so that is versatile with python formatting-->
  <p spkr="{gbl.chr[_player].name.common">Hey there</p>
</script>
```

selectors.xml
```
<root id="selector">

  <meta>
    <var>greetings</var>
    <var>goodbyes</var>
    <var>transitions</var>
  </meta>
  
  <sel id="greetings">
    <mood eg="1.0"><!--emotion; if vector component not listed then is 0, eg this is (1.0, 0, 0, 0)-->
      <p>Hi there {gbl.chr[_player].name.common}! How'ya doing?</p>
      <p>Hey there {gbl.chr[_player].name.common}, what's up?</p>
      <p>Heya!</p>
    </mood>
      
    <mood al="-1.0"><!--loathing-->
      <p>What the fuck do you want {gbl.chr[_player].name.proper}?</p>
      <p>You again?</p>
      <p>Honestly {gbl.chr[_player].name.common}, just stop pestering me!</p>
    </mood>
    
    <mood fr="1.0"><!--fear-->
      <p>BWAAAA!! Y-y-you scared me {gbl.chr[_player].name.common}!</p>
    </mood>
      
  </sel>
  
  <sel id="goodbyes">
    <mood eg="1.0">
      <p>See ya later!</p>
      <p>Let's talk again soon, {gbl.chr[_player].name.common}</p>
    </mood>
  </sel>
  
  <sel id="transitions">
    
    <mood><!--this is the zero emotion vector-->
      <p>By the way {gbl.chr[_player].name.common},</p>  
    </mood>
    
    <mood eg="-0.4" av="0.4"><!--embarassment-->
      <p>I-I u-umm, A-a-anyways,...</p>
    </mood>
    
  </sel>
    
</root>

```

4. basically the game is playing a recusive game of madlibs, where word-choice is affected by mood
  i. for selectors, choose selectors by mood, then choose randomly if multiple options
  ii. for constants, select correct variable from union TODO:: how to aggregate this?
  iii. for optionals, if cosine from dot product of emotions is above a THRESHOLD
		
# Emotion model
1. p2 (npc) thinks about T1 (topic)
  a. topic bumped to the top of "thoughts"
  b. all other topics shifted down
  c. initiated by player bringing up conversation
		
2. p2 current emotion vector is the AVERAGE of FIRST 5? topic emotion vectors
  a. essentially, npc's mood reflects average of latest 5? topics in her mind
		
3. every ~1 hour:
  a. npc pushes their default thought with 0.9 chance
  b. OR a random non-top non-defalt thought with 0.1 chance
		
3. basically, in short run, player controls short term mood of npc by talking about topics that npc has emotions for
4. in long run, npc's emotion reflect their default personality
		
# Character Storage

During runtime in python, a character json will be parsed and loaded as an object
```js
{
	"name":{
		"proper":"Mary Jane",//must be unique
		"common":"MJ",//also must be unique
	},
	
	"topic_emotion":{//describes 4-dimensional emotion for each topic, in order of "emotion" below
		//topics include: object-sets, activities, people (includes player), 
		//all player has a "default" emotion (personality) (see section: [Emotion Model])
		//these must be kept simple
		
		"pets":[0.9, 0.9, 0.0, -0.1],
		"_player": [0.9, 0.9, -0.8, -0.4], //basically this example npc is a tsundere
		"Jack Adams": [0.0, -1.0, -1.0, -1.0],//basically she hates Jack's guts
		"reading":[1.0, 1.0, 0.0, -1.0]//she loves reading
		
	},
	
	"common_emotion":{//miscellanous emotions, includes feelings from how conversation is held
		"personality":[0.2, 0.0, 0.0, 0.0],//her personality is being in serenity
		"dialogue_confusion":[0.0, -1.0, -1.0, 0.5],//she get's super pissed off from not understanding player
    
    //linear combinations of basis emotions
    "embarrassment":[-0.4, 0.0, 0.0, 0.4]
		
		
	}
	
	"thoughts":[//in order of how much they are thinking about them at the moment
		
		"default", "player", "pets", "reading", "Jack Adams" 
		//in this moment, perhaps it's been an hour since she last talked to player about reading, then pets.
		//she is now feeling emotions from default, player, and pets
	]
	
	"emotion":{//according to Plutchik's wheel of emotion
	
		//each half-pair is from 0.0 to 1.0 (emotion is 4-dimensional space)
		//by name, these are the most intense of their dimension and are only meaningful in pairs
		//each dimension has 7 divisions, with neutral being twice as large an interval than any other:
		//intervals [1.0, 0.75], (0.75, 0.5], (0.5, 0.25], (0.25, -0.25), [-0.25, -0.5), [-0.5, -0.75), [-0.75, -1.0]
		
		//eg
		"ecstacy":0.0,//joy, serenety, neutral
		"grief":0.0,//sadness, pensiveness, neutral
			
		//al
		"admiration":0.0,//trust, acceptance, neutral
		"loathing":0.0,//disgust, boredom, neutral

		//fr
		"fear":0.0,//terror, apprehensiveness, neutral
		"rage":0.0,//anger, annoyance, neutral
			
		//av
		"amazement":0.0,//surprise, distraction, neutral
		"vigilance":0.0//anticipation, interest, neutral
	}
	
}
```