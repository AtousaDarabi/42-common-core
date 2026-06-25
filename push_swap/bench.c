/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bench.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 18:11:09 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/25 16:45:24 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ft_printf(const char *format, ...);

static void	print_bench_ops(t_bench *b)
{
	ft_printf("[bench] sa: %d sb: %d ss: %d pa: %d pb: %d\n",
		b->sa, b->sb, b->ss, b->pa, b->pb);
	ft_printf("[bench] ra: %d rb: %d rr: %d rra: %d rrb: %d rrr: %d\n",
		b->ra, b->rb, b->rr, b->rra, b->rrb, b->rrr);
}

void	print_bench_results(t_bench *b)
{
	int	disorder_pct;

	disorder_pct = (int)(b->disorder * 100);
	ft_printf("[bench] disorder: %d.00%%\n", disorder_pct);
	ft_printf("[bench] strategy: Adaptive / O(n log n)\n");
	ft_printf("[bench] total_ops: %d\n", b->total_ops);
	print_bench_ops(b);
}
