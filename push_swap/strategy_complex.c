/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strategy_complex.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 21:10:13 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/09 21:11:35 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/* We find the maximum number of bits needed to represent all indices */
static int	get_max_bits(int size)
{
	int	max_bits;
	int	max_num;

	max_bits = 0;
	max_num = size - 1;
	while ((max_num >> max_bits) != 0)
		max_bits++;
	return (max_bits);
}

/* We implement a complex strategy for sorting using Radix Sort */
void	strategy_complex(t_stack **a, t_stack **b, t_bench *bnch, int size)
{
	int	i;
	int	j;
	int	max_bits;

	// We first assign an index to each number based on its value (0 for smallest, size-1 for largest)
	// We need these indices to perform the radix sort based on their binary representation
	void assign_indexes(t_stack *a, int size);
	assign_indexes(*a, size);
	
	max_bits = get_max_bits(size);
	i = 0;
	while (i < max_bits)
	{
		j = 0;
		while (j < size)
		{
			// We check the i-th bit of the index of the top element of A
			if ((((*a)->index >> i) & 1) == 1)
				ra(a, bnch);
			else
				pb(a, b, bnch); // We push it to B if the bit is 0
			j++;
		}
		// We then push all elements back from B to A, which will be in the correct order for this bit
		while (*b)
			pa(a, b, bnch);
		i++;
	}
}
