monzo_expense_categories_mappings = {
    "Food": ["Eating out", "Groceries"],
    "Gifts": ["Gifts", "Family"],
    "Health/medical": [],
    "Home": [],
    "Transportation": ["Transport"],
    "Personal": ["Entertainment", "Personal care"],
    "Pets": [],
    "Utilities": ["Bills"],
    "Travel": ["Holidays"],
    "Debt": ["Finances"],
    "Other": ["General", "Charity", "Shopping"],
    "Subscriptions": [],
}

expense_categories_mappings = {
    "Food": ["Food"],
    "Gifts": ["Gifts"],
    "Health/medical": ["Health/medical"],
    "Home": ["Home"],
    "Transportation": ["Transportation"],
    "Personal": ["Personal"],
    "Pets": ["Pets"],
    "Utilities": ["Utilities"],
    "Travel": ["Travel"],
    "Debt": ["Debt"],
    "Other": ["Other"],
    "Subscriptions": ["Subscriptions"],
}

monzo_income_categories_mapping = {
    "Savings": [],
    "Paycheck": ["Income"],
    "Bonus": [],
    "Interest": [],
    "Other": [],
}

income_categories_mapping = {
    "Savings": ["Savings"],
    "Paycheck": ["Paycheck"],
    "Bonus": ["Bonus"],
    "Interest": ["Interest"],
    "Other": ["Other"],
}

internal_transfers = {
    "description": [
        "Aqua",
        "BILL PAYMENT VIA FASTER PAYMENT TO PAUL MONZO REFERENCE TOP OP",
        "TRANSFER FROM MR PAUL OMAMEZI OLOGEH",
        "TRANSFER TO MR PAUL OMAMEZI OLOGEH",
        "TRANSFER FROM PAUL OLOGEH",
        "Internal Transfer",
        "PAYMENT RECEIVED - THANK YOU",
    ],
    "category": ["Transfers"],
}

for category in income_categories_mapping:
    if category in monzo_income_categories_mapping:
        income_categories_mapping[category] += monzo_income_categories_mapping[category]

for category in expense_categories_mappings:
    if category in monzo_expense_categories_mappings:
        expense_categories_mappings[category] += monzo_expense_categories_mappings[
            category
        ]

description_knowledge = {
    "INCOME": {
        "Savings": [],
        "Paycheck": ["PassFort"],
        "Bonus": [],
        "Interest": ["Interest"],
        "Other": [],
    },
    "EXPENSE": {
        "Food": ["Sainsbury", "Tesco", "Just Eat", "Dominos"],
        "Gifts": [],
        "Health/medical": [],
        "Home": [],
        "Transportation": ["Tfl Travel", "Uber", "Bolt", "Oyster"],
        "Personal": ["Amazon", "Vue"],
        "Pets": [],
        "Utilities": ["EE"],
        "Travel": [],
        "Debt": ["Overdraft"],
        "Other": [],
        "Subscriptions": ["Netflix", "Spotify"],
    },
}
