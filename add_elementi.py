#!/usr/bin/env python
# -*- coding: utf-8 -*-

# AMIU copyleft 2021
# Roberto Marzocchi

'''
Lo script interroga un elenco di piazzole


'''


import os, sys, getopt, re
from tkinter import E, Entry  # ,shutil,glob
import requests
from requests.exceptions import HTTPError




import json


import inspect, os.path




import psycopg2
import sqlite3


currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

sys.path.append('../')
from credenziali import *

#import requests
import datetime
import time

import ldap

import logging

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))

#tmpfolder=tempfile.gettempdir() # get the current temporary directory
logfile='{}/log/ldap.log'.format(path)
errorfile='{}/log/ldap_error.log'.format(path)
#if os.path.exists(logfile):
#    os.remove(logfile)

'''logging.basicConfig(
    #handlers=[logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')],
    format='%(asctime)s\t%(levelname)s\t%(message)s',
    #filemode='w', # overwrite or append
    #fileencoding='utf-8',
    #filename=logfile,
    level=logging.DEBUG)
'''




# Create a custom logger
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
    ]
)

logger = logging.getLogger()

# Create handlers
c_handler = logging.FileHandler(filename=errorfile, encoding='utf-8', mode='w')
f_handler = logging.StreamHandler()
#f_handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')


c_handler.setLevel(logging.ERROR)
f_handler.setLevel(logging.DEBUG)


# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


cc_format = logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s')

c_handler.setFormatter(cc_format)
f_handler.setFormatter(cc_format)



def main():
     #################################################################
    logger.info('Connessione al db SIT')
    conn = psycopg2.connect(dbname=db,
                        port=port,
                        user=user,
                        password=pwd,
                        host=host)

    curr = conn.cursor()
    curr1 = conn.cursor()
    #conn.autocommit = True
    ###################################################################


    #*************************************************************************************************************
    #   INPUT:
    #  - elenco piazzole con ordine
    #  - tipo di elemento da inserire
    #  - TODo (numero di elementi da inserire)
    #*************************************************************************************************************

    p1= '''
    join (values
    (1,20003  ),
(2,20044  ),
(3,20113  ),
(4,20116  ),
(5,20119  ),
(6,20121  ),
(7,20122  ),
(8,20124  ),
(9,20126  ),
(10,20127 ),
(11,20128 ),
(12,20129 ),
(13,20130 ),
(14,20132 ),
(15,20133 ),
(16,20134 ),
(17,20136 ),
(18,20157 ),
(19,20159 ),
(20,20163 ),
(21,20194 ),
(22,20197 ),
(23,20198 ),
(24,20199 ),
(25,20204 ),
(26,20207 ),
(27,20208 ),
(28,20209 ),
(29,20216 ),
(30,20219 ),
(31,20221 ),
(32,20222 ),
(33,20234 ),
(34,20238 ),
(35,20253 ),
(36,20278 ),
(37,20279 ),
(38,20305 ),
(39,20307 ),
(40,20309 ),
(41,20310 ),
(42,20386 ),
(43,20388 ),
(44,20391 ),
(45,20405 ),
(46,20406 ),
(47,20407 ),
(48,20437 ),
(49,20439 ),
(50,20458 ),
(51,20509 ),
(52,20510 ),
(53,20514 ),
(54,20515 ),
(55,20517 ),
(56,20519 ),
(57,20520 ),
(58,20521 ),
(59,20522 ),
(60,20523 ),
(61,20524 ),
(62,20529 ),
(63,20563 ),
(64,20564 ),
(65,20565 ),
(66,20572 ),
(67,20573 ),
(68,20574 ),
(69,20575 ),
(70,20578 ),
(71,20612 ),
(72,20613 ),
(73,20614 ),
(74,20615 ),
(75,20616 ),
(76,20727 ),
(77,20728 ),
(78,20729 ),
(79,20737 ),
(80,20738 ),
(81,20739 ),
(82,20742 ),
(83,20744 ),
(84,20745 ),
(85,20746 ),
(86,20747 ),
(87,20750 ),
(88,20752 ),
(89,20753 ),
(90,20833 ),
(91,20866 ),
(92,20895 ),
(93,20931 ),
(94,20951 ),
(95,20956 ),
(96,20963 ),
(97,20975 ),
(98,20979 ),
(99,20982 ),
(100,20983),
(101,20984),
(102,20985),
(103,20986),
(104,20987),
(105,20989),
(106,20991),
(107,20994),
(108,20996),
(109,20997),
(110,20998),
(111,20999),
(112,21000),
(113,21002),
(114,21016),
(115,21018),
(116,21023),
(117,21090),
(118,21115),
(119,21116),
(120,21117),
(121,21124),
(122,21127),
(123,21135),
(124,21137),
(125,21138),
(126,21140),
(127,21143),
(128,21249),
(129,21250),
(130,21251),
(131,21252),
(132,21254),
(133,21255),
(134,21256),
(135,21286),
(136,21287),
(137,21288),
(138,21290),
(139,21293),
(140,21299),
(141,21304),
(142,21316),
(143,21317),
(144,21319),
(145,21349),
(146,21350),
(147,21353),
(148,21354),
(149,21356),
(150,21357),
(151,21363),
(152,21399),
(153,21400),
(154,21406),
(155,21413),
(156,21419),
(157,21486),
(158,21487),
(159,21490),
(160,21492),
(161,21493),
(162,21496),
(163,21498),
(164,21500),
(165,21502),
(166,21503),
(167,21504),
(168,21505),
(169,21506),
(170,21510),
(171,21514),
(172,21517),
(173,21547),
(174,21574),
(175,21639),
(176,21642),
(177,21643),
(178,21644),
(179,21707),
(180,21722),
(181,21723),
(182,21724),
(183,21725),
(184,21727),
(185,21728),
(186,21731),
(187,21760),
(188,21761),
(189,21762),
(190,21763),
(191,21764),
(192,21765),
(193,21766),
(194,21773),
(195,21829),
(196,21830),
(197,21831),
(198,21863),
(199,21887),
(200,21888),
(201,21904),
(202,21905),
(203,21906),
(204,21948),
(205,21957),
(206,21959),
(207,21963),
(208,21965),
(209,22064),
(210,22065),
(211,22131),
(212,22132),
(213,22159),
(214,22196),
(215,22219),
(216,22238),
(217,22241),
(218,22242),
(219,22244),
(220,22245),
(221,22246),
(222,22254),
(223,22257),
(224,22262),
(225,22275),
(226,22281),
(227,22319),
(228,22369),
(229,22370),
(230,22378),
(231,22379),
(232,22380),
(233,22381),
(234,22383),
(235,22384),
(236,22422),
(237,22424),
(238,22443),
(239,22456),
(240,22458),
(241,22505),
(242,22507),
(243,22565),
(244,22566),
(245,22603),
(246,22626),
(247,22627),
(248,22631),
(249,22632),
(250,22697),
(251,22758),
(252,22795),
(253,22796),
(254,22797),
(255,22798),
(256,22817),
(257,22818),
(258,22849),
(259,22908),
(260,22975),
(261,22976),
(262,22977),
(263,22978),
(264,22979),
(265,22980),
(266,22984),
(267,22986),
(268,23033),
(269,23044),
(270,23063),
(271,23070),
(272,23073),
(273,23075),
(274,23076),
(275,23101),
(276,23102),
(277,23106),
(278,23109),
(279,23110),
(280,23114),
(281,23115),
(282,23116),
(283,23119),
(284,23121),
(285,23122),
(286,23127),
(287,23128),
(288,23180),
(289,23270),
(290,23271),
(291,23273),
(292,23279),
(293,23350),
(294,23354),
(295,23355),
(296,23365),
(297,23366),
(298,23370),
(299,23372),
(300,23376),
(301,23395),
(302,23413),
(303,23438),
(304,23439),
(305,23539),
(306,23540),
(307,23542),
(308,23630),
(309,23639),
(310,23640),
(311,23647),
(312,23680),
(313,23692),
(314,23693),
(315,23723),
(316,23726),
(317,23727),
(318,23729),
(319,23735),
(320,23736),
(321,23866),
(322,23986),
(323,23991),
(324,24031),
(325,24033),
(326,24034),
(327,24036),
(328,24037),
(329,24041),
(330,24062),
(331,24063),
(332,24108),
(333,24111),
(334,24113),
(335,24114),
(336,24116),
(337,24118),
(338,24120),
(339,24166),
(340,24167),
(341,24168),
(342,24171),
(343,24245),
(344,24348),
(345,24373),
(346,24375),
(347,24376),
(348,24378),
(349,24403),
(350,24404),
(351,24405),
(352,24406),
(353,24407),
(354,24408),
(355,24410),
(356,24411),
(357,24436),
(358,24437),
(359,24438),
(360,24441),
(361,24442),
(362,24448),
(363,24450),
(364,24454),
(365,24455),
(366,24457),
(367,24459),
(368,24462),
(369,24513),
(370,24514),
(371,24515),
(372,24517),
(373,24518),
(374,24519),
(375,24528),
(376,24530),
(377,24531),
(378,24532),
(379,24570),
(380,24602),
(381,24618),
(382,24619),
(383,24620),
(384,24621),
(385,24624),
(386,24626),
(387,24628),
(388,24664),
(389,24669),
(390,24701),
(391,24702),
(392,24703),
(393,24705),
(394,24706),
(395,24708),
(396,24710),
(397,24712),
(398,24714),
(399,24716),
(400,24773),
(401,24797),
(402,24838),
(403,24841),
(404,24842),
(405,24944),
(406,24967),
(407,24969),
(408,24970),
(409,24971),
(410,24973),
(411,24984),
(412,24985),
(413,24986),
(414,24990),
(415,24991),
(416,24994),
(417,24995),
(418,24996),
(419,24997),
(420,24998),
(421,25023),
(422,25026),
(423,25027),
(424,25031),
(425,25035),
(426,25036),
(427,25096),
(428,25125),
(429,25135),
(430,25136),
(431,25137),
(432,25142),
(433,25148),
(434,25149),
(435,25151),
(436,25152),
(437,25153),
(438,25154),
(439,25156),
(440,25157),
(441,25159),
(442,25164),
(443,25168),
(444,25174),
(445,25216),
(446,25219),
(447,25220),
(448,25221),
(449,25222),
(450,25223),
(451,25224),
(452,25225),
(453,25263),
(454,25266),
(455,25300),
(456,25301),
(457,25303),
(458,25305),
(459,25306),
(460,25307),
(461,25308),
(462,25309),
(463,25336),
(464,25369),
(465,25371),
(466,25372),
(467,25374),
(468,25377),
(469,25386),
(470,25501),
(471,25502),
(472,25503),
(473,25505),
(474,25506),
(475,25508),
(476,25518),
(477,25520),
(478,25521),
(479,25529),
(480,25530),
(481,25536),
(482,25538),
(483,25541),
(484,25543),
(485,25544),
(486,25545),
(487,25547),
(488,25548),
(489,25549),
(490,25552),
(491,25553),
(492,25560),
(493,25578),
(494,25582),
(495,25583),
(496,25587),
(497,25591),
(498,25596),
(499,25600),
(500,25604),
(501,25606),
(502,25608),
(503,25609),
(504,25642),
(505,25669),
(506,25678),
(507,25686),
(508,25722),
(509,25748),
(510,25751),
(511,25767),
(512,25768),
(513,25771),
(514,25772),
(515,25774),
(516,25775),
(517,25777),
(518,25778),
(519,25781),
(520,25782),
(521,25792),
(522,25793),
(523,25803),
(524,25804),
(525,25805),
(526,25806),
(527,25807),
(528,25822),
(529,25870),
(530,25872),
(531,25873),
(532,25874),
(533,25875),
(534,25876),
(535,25877),
(536,25878),
(537,25880),
(538,25882),
(539,25886),
(540,25888),
(541,25890),
(542,25946),
(543,25948),
(544,25949),
(545,25950),
(546,25951),
(547,25952),
(548,25953),
(549,25969),
(550,25971),
(551,26035),
(552,26039),
(553,26090),
(554,26091),
(555,26095),
(556,26098),
(557,26099),
(558,26104),
(559,26106),
(560,26110),
(561,26112),
(562,26114),
(563,26190),
(564,26191),
(565,26194),
(566,26218),
(567,26219),
(568,26234),
(569,26239),
(570,26240),
(571,26241),
(572,26265),
(573,26267),
(574,26268),
(575,26273),
(576,26276),
(577,26283),
(578,26284),
(579,26285),
(580,26288),
(581,26302),
(582,26303),
(583,26305),
(584,26306),
(585,26322),
(586,26328),
(587,26373),
(588,26374),
(589,26375),
(590,26377),
(591,26378),
(592,26382),
(593,26384),
(594,26386),
(595,26388),
(596,26391),
(597,26392),
(598,26406),
(599,26407),
(600,26409),
(601,26424),
(602,26425),
(603,26427),
(604,26433),
(605,26485),
(606,26486),
(607,26489),
(608,26498),
(609,26501),
(610,26502),
(611,26506),
(612,26507),
(613,26508),
(614,26509),
(615,26510),
(616,26511),
(617,26513),
(618,26515),
(619,26516),
(620,26565),
(621,26583),
(622,26589),
(623,26596),
(624,26600),
(625,26603),
(626,26605),
(627,26606),
(628,26607),
(629,26618),
(630,26619),
(631,26620),
(632,26621),
(633,26622),
(634,26626),
(635,26690),
(636,26691),
(637,26698),
(638,26700),
(639,26712),
(640,26715),
(641,26716),
(642,26719),
(643,26720),
(644,26725),
(645,26728),
(646,26747),
(647,26753),
(648,26754),
(649,26755),
(650,26756),
(651,26757),
(652,26758),
(653,26759),
(654,26760),
(655,26761),
(656,26776),
(657,26777),
(658,26791),
(659,26792),
(660,26795),
(661,26797),
(662,26799),
(663,26801),
(664,26803),
(665,26804),
(666,26809),
(667,26810),
(668,26812),
(669,26889),
(670,26891),
(671,26892),
(672,26893),
(673,26894),
(674,26895),
(675,26896),
(676,26897),
(677,26905),
(678,26907),
(679,26909),
(680,26911),
(681,26913),
(682,26954),
(683,26966),
(684,26972),
(685,26973),
(686,26974),
(687,26976),
(688,26979),
(689,26980),
(690,26985),
(691,26986),
(692,26987),
(693,26991),
(694,26996),
(695,26997),
(696,26998),
(697,26999),
(698,27016),
(699,27017),
(700,27018),
(701,27022),
(702,27023),
(703,27041),
(704,27042),
(705,27092),
(706,27093),
(707,27098),
(708,27118),
(709,27127),
(710,27128),
(711,27135),
(712,27136),
(713,27168),
(714,27169),
(715,27171),
(716,27193),
(717,27276),
(718,27358),
(719,27360),
(720,27361),
(721,27362),
(722,27363),
(723,27411),
(724,27429),
(725,27430),
(726,27431),
(727,27434),
(728,27435),
(729,27544),
(730,27545),
(731,27550),
(732,27552),
(733,27557),
(734,27558),
(735,27561),
(736,27563),
(737,27564),
(738,27573),
(739,27576),
(740,27577),
(741,27634),
(742,27635),
(743,27639),
(744,27673),
(745,27674),
(746,27675),
(747,27676),
(748,27677),
(749,27678),
(750,27679),
(751,27680),
(752,27681),
(753,27682),
(754,27683),
(755,27717),
(756,27718),
(757,27737),
(758,27750),
(759,27771),
(760,27772),
(761,27775),
(762,27778),
(763,27796),
(764,27797),
(765,27805),
(766,27806),
(767,27807),
(768,27808),
(769,27870),
(770,27874),
(771,27875),
(772,27878),
(773,27879),
(774,27880),
(775,27881),
(776,27884),
(777,27890),
(778,27892),
(779,27921),
(780,27922),
(781,27923),
(782,27924),
(783,27925),
(784,27964),
(785,27976),
(786,27977),
(787,27978),
(788,27979),
(789,27982),
(790,27991),
(791,28027),
(792,28028),
(793,28232),
(794,28234),
(795,28246),
(796,28249),
(797,28250),
(798,28251),
(799,28256),
(800,28257),
(801,28258),
(802,28259),
(803,28260),
(804,28261),
(805,28273),
(806,28275),
(807,28707),
(808,28713),
(809,28716),
(810,28717),
(811,28730),
(812,28732),
(813,28733),
(814,28741),
(815,28745),
(816,28750),
(817,28751),
(818,28762),
(819,28770),
(820,28857),
(821,29610),
(822,29612),
(823,29615),
(824,29703),
(825,29715),
(826,29716),
(827,29717),
(828,29732),
(829,29734),
(830,29746),
(831,29762),
(832,29768),
(833,29772),
(834,29945),
(835,29958),
(836,29959),
(837,30325),
(838,30373),
(839,30475),
(840,30492),
(841,30795),
(842,30796),
(843,30801),
(844,30804),
(845,30805),
(846,30806),
(847,30812),
(848,30817),
(849,30823),
(850,30837),
(851,30838),
(852,30852),
(853,30981),
(854,30988),
(855,30989),
(856,31006),
(857,31024),
(858,31055),
(859,31073),
(860,31091),
(861,31111),
(862,31118),
(863,31122),
(864,31125),
(865,31126),
(866,31143),
(867,31155),
(868,31185),
(869,31224),
(870,31246),
(871,31253),
(872,31255),
(873,31266),
(874,31290),
(875,31468),
(876,31469),
(877,31485),
(878,31490),
(879,31496),
(880,31519),
(881,31526),
(882,31529),
(883,31535),
(884,31563),
(885,31587),
(886,31588),
(887,31589),
(888,31599),
(889,31609),
(890,31620),
(891,31670),
(892,31671),
(893,31675),
(894,31676),
(895,31677),
(896,31680),
(897,31725),
(898,31729),
(899,31776),
(900,31806),
(901,33162),
(902,33181),
(903,33188),
(904,36992),
(905,36993),
(906,37100),
(907,37169),
(908,37301),
(909,37695),
(910,38233),
(911,38988),
(912,39419),
(913,39595),
(914,39612),
(915,39697),
(916,39748),
(917,39832),
(918,39968),
(919,40117),
(920,40118),
(921,40520),
(922,40521),
(923,40522),
(924,40523),
(925,40524),
(926,40525),
(927,40526),
(928,40965),
(929,41014),
(930,41167),
(931,41221),
(932,41258),
(933,41299),
(934,41310),
(935,41311),
(936,41359),
(937,41369),
(938,41524),
(939,41525),
(940,41526),
(941,41527),
(942,41528),
(943,41529),
(944,41531),
(945,41533),
(946,41534),
(947,41535),
(948,41539),
(949,41540),
(950,41541),
(951,41543),
(952,41561),
(953,41565),
(954,41575),
(955,41583),
(956,41631),
(957,41633),
(958,41635),
(959,41636),
(960,41667),
(961,41674),
(962,41681),
(963,41694),
(964,41711),
(965,41756),
(966,41758),
(967,41798),
(968,41898)
    ) as p1 (id, piazzola)
    '''

    tipo_elemento='RIORDINO_PIAZZOLA'



    #   FINE INPUT
    #*************************************************************************************************************

    query_select0='''SELECT tipo_elemento, tipo_rifiuto FROM elem.tipi_elemento te WHERE nome ilike %s'''

    try:
        curr.execute(query_select0, (tipo_elemento,))
        id_tipo=curr.fetchall()
    except Exception as e:
        logger.error(e)

    id_t=0
    for it in id_tipo:
        id_t=it[0]
        tr=it[1]
    if id_t==0:
        logger.error('Controlla il tipo elemento {} che sembra non esistere'.format(tipo_elemento))
        exit()


    curr.close()
    curr = conn.cursor()


    # faccio insert solo se già non ci fosse una elemento dello stesso rifiuto
    """query_select='''
    select id, id_piazzola, via, riferimento from
(select id, id_piazzola, via, riferimento, sum(num)
from (  
select
p1.id, e.id_piazzola, v.nome as via,
p2.numero_civico as civ, p2.riferimento, 
case 
when te.nome is null then 'ND'
else te.nome
end nome
, 
count(te.tipo_elemento) as num
from elem.piazzole p2
left join elem.elementi e on p2.id_piazzola = e.id_piazzola 
left join elem.aste a on a.id_asta = p2.id_asta 
left join topo.vie v on v.id_via = a.id_via 
left join elem.tipi_elemento te on te.tipo_elemento = e.tipo_elemento and te.tipo_rifiuto IN (%s) 
{} on p2.id_piazzola = p1.piazzola 
group by
e.id_piazzola, v.nome, p2.numero_civico, p2.riferimento, te.nome, p1.id 
order by
p1.id
) ppp
group by id, id_piazzola, via, riferimento
) pppp where sum = 0
order by id'''.format(p1)"""

    # faccio insert in tutti i casi
    query_select='''
        select id, id_piazzola, via, riferimento from
    (select id, id_piazzola, via, riferimento, sum(num)
    from (  
    select
    p1.id, e.id_piazzola, v.nome as via,
    p2.numero_civico as civ, p2.riferimento, 
    case 
    when te.nome is null then 'ND'
    else te.nome
    end nome
    , 
    count(te.tipo_elemento) as num
    from elem.piazzole p2
    left join elem.elementi e on p2.id_piazzola = e.id_piazzola 
    left join elem.aste a on a.id_asta = p2.id_asta 
    left join topo.vie v on v.id_via = a.id_via 
    left join elem.tipi_elemento te on te.tipo_elemento = e.tipo_elemento and te.tipo_rifiuto IN (%s) 
    {} on p2.id_piazzola = p1.piazzola 
    group by
    e.id_piazzola, v.nome, p2.numero_civico, p2.riferimento, te.nome, p1.id 
    order by
    p1.id
    ) ppp
    group by id, id_piazzola, via, riferimento
    ) pppp
    order by id'''.format(p1)




    #logger.debug(query_select)
    try:
        curr.execute(query_select, (tr,))
        piazzole_da_completare=curr.fetchall()
    except Exception as e:
        logger.error(e)

    for pp in piazzole_da_completare:
        #id_piazzola=pp[1]
        logger.info('Aggiunta un bidone {0} su piazzola {1}'.format(tipo_elemento, pp[1]))
        insert_query='''
        INSERT INTO elem.elementi
            (tipo_elemento, 
            id_piazzola, 
            id_asta, 
            x_id_cliente, 
            privato, peso_reale, peso_stimato,
            id_utenza,
            modificato_da,
            data_ultima_modifica, 
            percent_riempimento, 
            freq_stimata, 
            data_inserimento)
            values
            (%s, 
            %s, 
            (select id_asta from elem.piazzole where id_piazzola=%s), 
            '-1'::integer,
            0, 0, 0,
            '-1'::integer,
            '',
            now(), 
            90, 
            3,
            now()
            );'''
        try:
            curr1.execute(insert_query, (id_t,pp[1], pp[1]))
        except Exception as e:
            logger.error(e)

    if len(piazzole_da_completare)==0:
        logger.warning('NON ci sono piazzole da completare')
        exit()

    if input("Sei sicuro di voler continuare ed eseguire il COMMIT (operazione IRREVERSIBILE se non a mano)? [y / other]") == "y":
        logger.info("Eseguo il commit")
        conn.commit()
    else: 
        logger.warning("Sono uscito senza fare nullan")

        
    curr1.close()
    curr.close()
    conn.close()



if __name__ == "__main__":
    main() 