/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strategy_medium.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 21:09:13 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/09 21:32:19 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/* مقداردهی به ایندکس هر گره بر اساس ارزش عددی آن */
void	assign_indexes(t_stack *a)
{
	t_stack	*curr;
	t_stack	*compare;
	int		idx;

	curr = a;
	while (curr)
	{
		idx = 0;
		compare = a;
		while (compare)
		{
			if (curr->value > compare->value)
				idx++;
			compare = compare->next;
		}
		curr->index = idx;
		curr = curr->next;
	}
}

/* پیدا کردن پوزیشن گره‌ای با بالاترین ایندکس در استک */
static int	find_max_index_pos(t_stack *stack, int max_idx)
{
	int	pos;

	pos = 0;
	while (stack)
	{
		if (stack->index == max_idx)
			return (pos);
		pos++;
		stack = stack->next;
	}
	return (-1);
}

/* برگرداندن اعداد از استک B به A به صورت کاملاً مرتب شده */
static void	push_back_to_a(t_stack **a, t_stack **b, t_bench *bnch, int size)
{
	int	i;
	int	pos;

	i = size - 1;
	while (i >= 0)
	{
		pos = find_max_index_pos(*b, i);
		if (pos <= (i / 2))
		{
			while ((*b)->index != i)
				rb(b, bnch);
		}
		else
		{
			while ((*b)->index != i)
				rrb(b, bnch);
		}
		pa(a, b, bnch);
		i--;
	}
}

/* الگوریتم اصلی Chunk Sorting برای ۱۰۰ عدد */
void	strategy_medium(t_stack **a, t_stack **b, t_bench *bnch, int size)
{
	int	chunk_size;
	int	i;

	assign_indexes(*a);
	// بر اساس تئوری، سایز چانک مناسب برای ۱۰۰ عدد حدود ۱۵ الی ۲۰ هست
	chunk_size = 15; 
	i = 0;
	while (*a)
	{
		if ((*a)->index <= i)
		{
			pb(a, b, bnch);
			rb(b, bnch); // المان‌های خیلی کوچکتر رو می‌فرستیم ته استک ب
			i++;
		}
		else if ((*a)->index <= i + chunk_size)
		{
			pb(a, b, bnch);
			i++;
		}
		else
			ra(a, bnch);
	}
	push_back_to_a(a, b, bnch, size);
}
