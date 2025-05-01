
print(f"Loading constants...", flush=True, end='')

N_TASKS = 6
N_ATTRIBUTES = 7
ISSUE_IDEOLOGY = ['liberal', 'conservative']
CANDIDATE_PARTY = ['Democratic Party', 'Republican Party', 'Independent']
VARS = {
    'rid'         : 'User ID',
    'rid2'        : "User ID (long)",
    'duration_min': "Duration (in minutes)",
    'chk2_passed' : "Passed attention check (post-conjoint)",

    'status_threat' : 'Status threat exposure',

    'task'                : "Task",
    'chc'                 : "Candidate selected (original)",
    'chc_stack'           : "Candidate selected",
    'cand'                : 'Candidate',
    'chr'                 : "Candidate rate",

    'pty_pair'            : "Party affiliation pair",
    'pty_pair_ordered'    : "Party affiliation pair (ordered)",
    'pty_pair_group'      : "Partisan vs non-partisan pair",

    'c_party_affiliation' : "Party affiliation",
    'c_aff_ac'            : "Affirmative action",
    'c_trade'             : "Trade with China",
    'c_abortion'          : "Abortion",
    'c_immig'             : "Immigration",
    'c_lgbt'              : "LGBT rights",
    'c_red'               : "Redistribution",

    'c_ncons'             : 'Number of conservative positions',

    'c_aff_ac_s'            : "Affirmative action (statement)",
    'c_trade_s'             : "Trade with China (statement)",
    'c_abortion_s'          : "Abortion (statement)",
    'c_immig_s'             : "Immigration (statement)",
    'c_lgbt_s'              : "LGBT rights (statement)",
    'c_red_s'               : "Redistribution (statement)",

    # 
    'male'     : 'Male',
    'age'      : 'Age',
    'age_std'  : 'Age (std)',
    'educ'     : 'Education',
    'educ_std' : 'Education (std)',
    'inc'      : "Income (12 levels)",
    'inc_std'  : 'income (12 levels, std)',
    'state'    : "State",

    'pid'     : "Partisanship", 
    'pids'    : "Partisanship (strenght)",
    'psid'    : "Partisanship (social identity)",

    'wi'      : 'White identity',
    'ni'      : 'National identity',

    'conlib_std' : "Liberal-conservative (std)",
    'ideo_std'   : "Left-Right (std)",

    'ssp_white_minority' : "Perception: Whites becoming minority",
    'ssp_white_status'   : 'Perception: Whites loosing social status',
    'ssp_white_econ'     : 'Perception: Whites loosing economic stauts',
    'ssp_us_leader'      : 'Perception: US no longer global leader',
    'ssp_us_status'      : "Perception: Americans loosing social status",
    'ssp_us_econ'        : "Perception: Americans loosing economic status",

    'sa_diversity_threat' : "Feel threatened by ethnic diversity",
    'sa_diversity_benefit': 'Feel benefit from ethnic diversity',
    'sa_us_comp_threat'   : 'Feel threatened by other countries',
    'sa_us_comp_benefit'  : 'Feel benefit from other countries',

    'gp_white'  : 'Feels toward white Americans',
    'gp_black'  : 'Feels toward black Americans',
    'gp_latino' : 'Feels toward Latino Americans',
    'gp_asian'  : 'Feels toward Asian Americans',
    'gp_usa'    : 'Feels toward The United States',
    'gp_china'  : 'Feels toward China',
    'gp_uk'     : 'Feels toward The United Kingdom',
    'gp_japan'  : 'Feels toward Japan',
    'gp'        : "Generalized prejudice",

    'mc'            : 'Manipulation check (raw)',
    "mc_group"      : 'Manipulation check (group)',
    "mc_perc_corr"  : 'Manipulation check (percentage correct)',
    "mc_perc_incorr": 'Manipulation check (percentage incorrect)',
    "mc_score"      : 'Manipulation check score (% correct - % incorrect)',
}
ISSUES = ['c_aff_ac', 'c_trade', 'c_abortion', 'c_immig', 'c_lgbt', 'c_red']
ADJ_VARS = ['male', 'age_std', 'educ_std', 'inc_std']

# candidate issue_statements
PARTY = {
        "label": 'Party affiliation',
    "party": CANDIDATE_PARTY 
}
ABORTION = {
    "label": 'Abortion rights',
    "liberal": [
        "I advocate for people's right to make their own decisions about abortion.",
        "I am convinced that abortion must be a private decision, not a legal debate.",
        "I strongly believe that supporting abortion rights means supporting equality and freedom.",
        "I believe that abortion rights should be citizens' rights.",
        "In my view, choice over abortion should be a fundamental human right."
    ],
    "conservative": [
        "I strongly believe that abortion should be prohibited. We should protect human life at all stages.",
        "I believe that abortion is never a solution. Every unborn child has the inherent right to live.",
        "I am convinced that abortion undermines the value of human life. Therefore, I firmly believe that abortion should be restricted.",
        "If elected, I will defend my commitment to preserving the sanctity of life, not abortion.",
        "In my view, abortion is not a solution but another problem. I am in favor of protecting human life at all stages."
    ]
}
LGBT = {
    "label": 'Marriage and LGBT rights',
    "liberal": [
        "I strongly believe that equal rights and protections must include the LGBT community.",
        "I believe that LGBT individuals deserve the same legal protections as everyone else.",
        "I support LGBT rights because, for me, it means supporting human rights.",
        "I am convinced that if we respect human rights, we must respect LGBT rights.",
        "I believe that celebrating diversity means standing for LGBT rights."
    ],
    "conservative": [
        "I believe marriage should remain between a man and a woman.",
        "I believe that preserving traditional family values includes opposing LGBT marriage laws.",
        "LGBT rights challenge the traditional structure of our society, so I oppose it.",
        "I support upholding societal norms which preclude same-sex marriage.",
        "I strongly believe that endorsing LGBT rights might erode the family, cultural, and moral foundations of our society."
    ]
}
AFF_AC = {
    "label": 'Affirmative action',
    "liberal": [
        "I am certain that affirmative action is a necessary pathway to social and racial equality. Therefore, I support adopting more affirmative action policies that benefit African American and Latinos in this country.",
        "I stand for promoting diversity and inclusiveness through affirmative action to improve lives of African American and Latinos.",
        "I maintain that affirmative action rectifies historical injustices and systemic discrimination against minorities like African Americans and Latinos.",
        "I am convinced that affirmative action is a vital step toward a fair society with more inclusivity for African Americans and Latinos.",
        "I hold that supporting affirmative action means supporting equal opportunities for all, including minorities like African Americans and Latinos."
    ],
    "conservative": [
        "In my opinion, affirmative action can lead to reverse discrimination against whites. Therefore, affirmative action policies must be reduced.",
        "I firmly believe that selection should be based on individual merit, not affirmative action because affirmative action hurts white American majorities.",
        "In my view, affirmative action can undermine the principle of reward on merit and end up undermining chances of success for people in majority groups, like white Americans.",
        "In my view, affirmative action is detrimental to our society in the long run and hurt white American majorities. I believe in equal opportunity, not mandated equal results from affirmative action.",
        "I hold that affirmative action compromises standards of excellence and can reward minority groups even when they don't deserve it, at the expenses of deserving people among white Americans."
    ]
}
IMMIG = {
    "label": 'Immigration policy',
    "liberal": [
        "In my view, opening our borders to immigrants is a testament to our values of compassion and equality.",
        "I am certain that immigrants contribute enormously to our economic growth and cultural diversity.",
        "I am convinced that more immigrants can lead to more diversity and richness in our culture and society.",
        "Immigration is the backbone of our nation's history and should be celebrated.",
        "Immigrants bring unique skills and perspectives that benefit our economy."
    ],
    "conservative": [
        "A stricter immigration policy is necessary to protect our jobs and resources.",
        "I am certain that unregulated immigration could strain our public services and infrastructure.",
        "Protecting our borders is critical for our national security. We should have stronger policies against illegal immigration.",
        "The priority should be on taking care of our citizens before accepting more immigrants.",
        "It is crucial to control our borders and restrict immigration to protect our social values and culture."
    ]
}
RED = {
    "label": 'Redistribution',
    "liberal": [
        "I have no doubt that progressive taxation is an effective tool to reduce economic inequality. We must increase taxes on the rich and expand social programs.",
        "I am certain that raising taxes on the wealthy is a good thing. It can help to improve society by funding social welfare programs.",
        "I maintain that increasing taxes on capital gains to create more welfare policies could reduce wealth disparities.",
        "I support increasing tax on the wealthy to redistribute income and curb extreme wealth inequalities in our nation.",
        "I believe that tax reform targeting the rich could help to adopt more programs to help the poor and alleviate economic inequality."
    ],
    "conservative": [
        "I am certain that high taxes can discourage investment and hinder economic growth. I firmly oppose it. We already spend too much on welfare programs.",
        "I have no doubt that increasing taxes on the wealthy might drive them to invest elsewhere, which will hurt our economy. We should reduce government spending on welfare, not increase it.",
        "I have no doubt that progressive taxation could punish successful entrepreneurs and business owners. We should avoid increasing taxes at all costs.",
        "I hold that addressing economic inequality should not be achieved at the expense of economic growth. So, I oppose expanding welfare programs.",
        "I am convinced that tax policies should not unduly penalize the wealthy for their success, so I oppose increasing taxes to pay for welfare programs."
    ]
}
TRADE = {
    "label": 'Trade policy',
    "liberal": [
        "If elected, I will support open trade with other countries, like China, because it stimulates economic growth and development.",
        "I am sure that increasing trade with China is good because it creates a wider market for our products.",
        "I support reducing trade barriers against China. This will benefit our economy.",
        "I support global trade with China because it brings opportunities for businesses in our country to grow and expand.",
        "I have no doubt that promoting free trade with China encourages economic activity and job creation."
    ],
    "conservative": [
        "I support trade protectionism against China. We need to shield our local industries that make our country great.",
        "Increasing tariffs on Chinese products is needed to protect domestic jobs and our great economy.",
        "Stricter trade policies against China will prevent unfair competition from cheap foreign goods. This will help to maintain US economy, which is the leading in the world.",
        "I believe we need to prioritize our national industries before international trade with China to protect jobs and our world-leading economy.",
        "I am certain that free trade agreements with China can harm our local industries and employment. US has the largest economy in the world, and we must keep it that way."
    ]
}
ISSUE_STATEMENTS = {
    "abortion": ABORTION,
    "lgbt"    : LGBT,
    "aff_ac"  : AFF_AC,
    "red"     : RED,
    "trade"   : TRADE,
    "immig"   : IMMIG
}
# issue_statements

COLORS = {"Democratic voter":'#00AEF3',
          "Republican voter":'#E81B23'
          }

print('done!')
