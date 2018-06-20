from equity_for_dcf import get_coe_capm
from equity_for_dcf import get_mv_equity
from debt_for_dcf import get_mv_debt
from debt_for_dcf import get_debt_yield
from debt_for_dcf import get_tax
from fcf_for_dcf import get_starting_fcf
from fcf_for_dcf import get_fcf_growth
from equity_for_dcf import get_shares_outstanding


def dcf(stock):
    cost_of_equity = get_coe_capm(stock)
    cost_of_equity_print = round(cost_of_equity*100, 2)
    print('Your calculated cost of equity using the CAPM model is ', cost_of_equity_print, '%.')
    cost_of_debt = get_debt_yield(stock)/100.0
    cost_of_debt_print = round(cost_of_debt*100, 2)
    print('Your calculated cost of debt using average of current corporate debt is ', cost_of_debt_print, '%.')
    mv_debt_mils = get_mv_debt(stock)
    print('The market value of $', stock.upper(), ' debt in millions is ', round(mv_debt_mils, 2))
    mv_equity_mils = get_mv_equity(stock)
    print('The market value of $', stock.upper(), ' equity in millions is ', mv_equity_mils)

    total = mv_debt_mils+mv_equity_mils
    ratio_debt = mv_debt_mils/total
    ratio_equity = mv_equity_mils/total
    tax = get_tax(stock)
    tax_print = round(tax*100, 2)
    wacc = ratio_debt*cost_of_debt*(1-tax) + ratio_equity*cost_of_equity
    wacc_print = round(wacc*100, 2)

    print('Appropriate weighted average cost of capital (WACC) for $', stock.upper(), ' at a tax rate of ', tax_print,
          '% is ', wacc_print, '%.')
    start_fcf = get_starting_fcf(stock)
    start_fcf_print = round(start_fcf/1000000.0, 2)
    fcf_growth = get_fcf_growth(stock)
    fcf_growth_print = round(fcf_growth*100, 2)
    t_growth = .03
    t_growth_print = t_growth*100
    ent_val = pv_growing_annuity_with_tcf(start_fcf, fcf_growth, wacc, 4, t_growth)
    ent_val_print = round(ent_val/1000000.0, 2)
    print('Enterprise value of $', stock.upper(), 'in millions is ', ent_val_print, ' with a starting fcf of ',
          start_fcf_print, '(millions), an initial fcf growth rate of ', fcf_growth_print,
          '%, and a terminal growth rate of ', t_growth_print, '%.')
    equity_val = ent_val - mv_debt_mils*1000000
    equity_val_print = round(equity_val/1000000, 2)
    print('Equity value in millions of $', stock.upper(), 'is ', equity_val_print)
    s_outstanding = get_shares_outstanding(stock)
    share_price = equity_val/s_outstanding
    print('Estimated value of $', stock.upper(), ' is $', share_price, 'per share')


def pv_growing_annuity_with_tcf(start_val, growth_rate, discount_rate, length, term_growth):
    cf_list = []
    for index in range(0, length):
        cf = start_val*((1+growth_rate)**index)
        post_discount = cf/((1+discount_rate)**index)
        cf_list.append(post_discount)
    tcf = (cf_list[-1]*(1+term_growth))/(discount_rate-term_growth)
    cf_list.append(tcf)
    pv = sum(cf_list)
    return pv
