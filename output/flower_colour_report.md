# Do flower colours line up with the text?

Pre-registration: `analyses/flower_colour_prereg.md`. Colours: `analyses/flower_colours.csv`. 86 herbal pages with a single flower colour; colour labels shuffled within Currier language, 10,000 times, seed 20261003.

- Pages per colour: {np.str_('white'): 19, np.str_('blue'): 50, np.str_('red'): 10, np.str_('green'): 6, np.str_('yellow'): 1}
- Same-colour minus different-colour text similarity: **-0.0083** (shuffled -0.0008); p = 0.741 → **NOT SUPPORTED**

## Opening words by colour (descriptive)

- **blue** (50): koaiin (f3v), pchooiin (f4v), koary (f6v), fochor (f9v), pchocthy (f10r), paiin (f10v), tshol (f11r), torshor (f13r), koair (f13v), fshody (f17r), pdrairdy (f18r), pchor (f19r), pochaiin (f19v), faiis (f20v), toldshy (f21v), pydchdom (f23r), podairol (f23v), tchodar (f24v), psheoky (f26r), pchedar (f26v), kooiin (f29v), okeeesy (f30r), fchaiin (f32r), kcheodaiin (f32v), tar (f33v), oo (f35r), parchor (f35v), tshody (f37v), okchop (f38v), tedo (f39r), pdair (f39v), pchey (f40r), pcheody (f41v), tshodpy (f44r), pykydal (f45r), korary (f45v), psheot (f47v), pcheodchy (f48v), kshor (f49v), psheor (f50r), tchy (f50v), poshody (f51v), tdokchcfhy (f52r), pcheodar (f54v), kcheedchdy (f55v), ochal (f56r), kcheat (f56v), poeeockhey (f57r), cphy (f65v), okeodof (f66v)
- **green** (6): foar (f6r), kshol (f28v), tshdar (f33r), pcheoepchy (f34r), pshey (f41r), pchor (f52v)
- **red** (10): k (f5v), polyshy (f7v), tydlo (f9r), pcho (f14r), pocheody (f16r), pchodol (f17v), posaiin (f29r), tocphol (f37r), tsholdchy (f51r), kodam (f53r)
- **white** (19): kydainy (f2r), kooiin (f2v), pdychoiin (f14v), tshor (f15r), poror (f15v), told (f18v), por (f24r), pochof (f27v), pchodar (f28r), sain (f30v), keedey (f31r), ke'chdy (f34v), pchar (f36v), tarodaiin (f43r), pdsairy (f43v), tsho (f44v), pcheocphy (f46r), pshdaiin (f48r), podaiin (f54r)
- **yellow** (1): pchadan (f36r)

## Reading the result

- **Not supported.** Pages whose flowers share a colour do not share more vocabulary than pages with different
  colours (−0.008 vs −0.001 shuffled; p = 0.74).
- Blue dominates (50 of 86 single-colour pages), so most comparisons are blue against the rest. With only 1 yellow
  and 6 green pages, those colours could not show a pattern either way.
- Caveats: the colours were judged by eye at low resolution, ink colours have faded or changed over 600 years, and a
  colour-to-planet code might use something other than overall vocabulary (a single key word, for example).
- Taken at face value, the text of a plant page does not reflect its flower colour.
