/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   operations_one.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 21:03:50 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/09 21:03:53 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sa(t_stack **a, t_bench *b)
{
	t_stack	*first;
	t_stack	*second;

	if (!a || !*a || !(*a)->next)
		return ;
	first = *a;
	second = first->next;
	first->next = second->next;
	second->next = first;
	*a = second;
	if (b && b->active)
		b->sa++;
	else
		write(1, "sa\n", 3);
	if (b)
		b->total_ops++;
}

void	sb(t_stack **b_stk, t_bench *b)
{
	t_stack	*first;
	t_stack	*second;

	if (!b_stk || !*b_stk || !(*b_stk)->next)
		return ;
	first = *b_stk;
	second = first->next;
	first->next = second->next;
	second->next = first;
	*b_stk = second;
	if (b && b->active)
		b->sb++;
	else
		write(1, "sb\n", 3);
	if (b)
		b->total_ops++;
}

void	ss(t_stack **a, t_stack **b_stk, t_bench *bnch)
{
	int	prev_active;

	if (bnch)
	{
		prev_active = bnch->active;
		bnch->active = 1;
	}
	sa(a, bnch);
	sb(b_stk, bnch);
	if (bnch)
	{
		bnch->active = prev_active;
		if (bnch->active)
			bnch->ss++;
		else
			write(1, "ss\n", 3);
		bnch->total_ops--; /* چون دوتا حرکت قبلی هرکدام یک واحد اضافه کردن، یکی کم میکنیم */
	}
	else
		write(1, "ss\n", 3);
}

void	pa(t_stack **a, t_stack **b, t_bench *bnch)
{
	t_stack	*tmp;

	if (!b || !*b)
		return ;
	tmp = *b;
	*b = (*b)->next;
	tmp->next = *a;
	*a = tmp;
	if (bnch && bnch->active)
		bnch->pa++;
	else
		write(1, "pa\n", 3);
	if (bnch)
		bnch->total_ops++;
}

void	pb(t_stack **a, t_stack **b, t_bench *bnch)
{
	t_stack	*tmp;

	if (!a || !*a)
		return ;
	tmp = *a;
	*a = (*a)->next;
	tmp->next = *b;
	*b = tmp;
	if (bnch && bnch->active)
		bnch->pb++;
	else
		write(1, "pb\n", 3);
	if (bnch)
		bnch->total_ops++;
}
