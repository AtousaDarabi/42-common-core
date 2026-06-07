/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 21:06:16 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/09 21:06:40 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	print_error_and_exit(t_stack **a, int *arr)
{
	t_stack	*tmp;

	if (arr)
		free(arr);
	while (a && *a)
	{
		tmp = (*a)->next;
		free(*a);
		*a = tmp;
	}
	write(2, "Error\n", 6);
	exit(1);
}

static int	is_valid_number(char *str)
{
	int	i;

	i = 0;
	if (str[i] == '-' || str[i] == '+')
		i++;
	if (!str[i])
		return (0);
	while (str[i])
	{
		if (str[i] < '0' || str[i] > '9')
			return (0);
		i++;
	}
	return (1);
}

static long	ft_atoi_long(char *str, t_stack **a, int *arr)
{
	long	res;
	int		sign;
	int		i;

	res = 0;
	sign = 1;
	i = 0;
	if (str[i] == '-' || str[i] == '+')
	{
		if (str[i] == '-')
			sign = -1;
		i++;
	}
	while (str[i])
	{
		res = res * 10 + (str[i] - '0');
		if ((sign == 1 && res > 2147483647)
			|| (sign == -1 && (-res) < -2147483648))
			print_error_and_exit(a, arr);
		i++;
	}
	return (res * sign);
}

static void	check_duplicate(t_stack *a, int val, int *arr)
{
	while (a)
	{
		if (a->value == val)
			print_error_and_exit(&a, arr);
		a = a->next;
	}
}

int	*parse_arguments(int argc, char **argv, t_stack **a, int *size)
{
	int		i;
	int		*arr;
	t_stack	*new_node;
	t_stack	*curr;

	*size = argc - 1;
	arr = malloc(sizeof(int) * (*size));
	if (!arr)
		print_error_and_exit(a, NULL);
	i = 0;
	while (i < *size)
	{
		if (!is_valid_number(argv[i + 1]))
			print_error_and_exit(a, arr);
		arr[i] = (int)ft_atoi_long(argv[i + 1], a, arr);
		check_duplicate(*a, arr[i], arr);
		new_node = malloc(sizeof(t_stack));
		if (!new_node)
			print_error_and_exit(a, arr);
		new_node->value = arr[i];
		new_node->index = 0;
		new_node->next = NULL;
		if (!*a)
			*a = new_node;
		else
			curr->next = new_node;
		curr = new_node;
		i++;
	}
	return (arr);
}
