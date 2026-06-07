/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strategy_adaptive.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 21:11:54 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/09 21:12:20 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	strategy_adaptive(t_stack **a, t_stack **b, t_bench *bnch, int size)
{
	double	disorder;
	int		*arr;
	int		i;
	t_stack	*curr;

	if (size <= 1)
		return ;
	// We create an array to compute the disorder of the input, which is the ratio of inversions to total pairs
	arr = malloc(sizeof(int) * size);
	if (!arr)
		return ;
	curr = *a;
	i = 0;
	while (curr)
	{
		arr[i++] = curr->value;
		curr = curr->next;
	}
	disorder = compute_disorder(arr, size);
	free(arr);

	// We choose the strategy based on the size of the input and its disorder
	if (size <= 5 || disorder < 0.15)
		strategy_simple(a, b, bnch, size);
	else if (size <= 100 && disorder < 0.50)
		strategy_medium(a, b, bnch, size);
	else
		strategy_complex(a, b, bnch, size);
}
