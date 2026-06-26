/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker_bonus.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jukohler <jukohler@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 00:00:00 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/26 11:10:27 by jukohler         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker_bonus.h"

int	read_line(char *buf, int size)
{
	int		i;
	char	c;
	int		ret;

	i = 0;
	while (i < size - 1)
	{
		ret = read(0, &c, 1);
		if (ret <= 0)
			break ;
		buf[i++] = c;
		if (c == '\n')
			break ;
	}
	buf[i] = '\0';
	return (i > 0);
}

static int	apply_op_extend(char *op, t_stack **a, t_stack **b)
{
	if (op[0] == 'r' && op[1] == 'r' && op[2] == 'a' && op[3] == '\n')
		reverse_rotate(a);
	else if (op[0] == 'r' && op[1] == 'r' && op[2] == 'b' && op[3] == '\n')
		reverse_rotate(b);
	else if (op[0] == 'r' && op[1] == 'r' && op[2] == 'r' && op[3] == '\n')
	{
		reverse_rotate(a);
		reverse_rotate(b);
	}
	else
		return (0);
	return (1);
}

int	apply_op(char *op, t_stack **a, t_stack **b)
{
	if (op[0] == 's' && op[1] == 'a' && op[2] == '\n' && !op[3])
		swap(a);
	else if (op[0] == 's' && op[1] == 'b' && op[2] == '\n' && !op[3])
		swap(b);
	else if (op[0] == 's' && op[1] == 's' && op[2] == '\n' && !op[3])
	{
		swap(a);
		swap(b);
	}
	else if (op[0] == 'p' && op[1] == 'a' && op[2] == '\n' && !op[3])
		push(a, b);
	else if (op[0] == 'p' && op[1] == 'b' && op[2] == '\n' && !op[3])
		push(b, a);
	else if (op[0] == 'r' && op[1] == 'a' && op[2] == '\n' && !op[3])
		rotate(a);
	else if (op[0] == 'r' && op[1] == 'b' && op[2] == '\n' && !op[3])
		rotate(b);
	else if (op[0] == 'r' && op[1] == 'r' && op[2] == '\n' && !op[3])
	{
		rotate(a);
		rotate(b);
	}
	else
		return (apply_op_extend(op, a, b));
	return (1);
}

static int	run_checker(t_stack **a, t_stack **b)
{
	char	op[8];

	while (read_line(op, 8))
	{
		if (op[0] == '\n' && !op[1])
		{
			ft_putstr_fd("\033[A", 1);
			break ;
		}
		if (!apply_op(op, a, b))
		{
			ft_putstr_fd("Error\n", 2);
			return (1);
		}
	}
	if (is_sorted(*a) && *b == NULL)
		ft_putstr_fd("OK\n", 1);
	else
		ft_putstr_fd("KO\n", 1);
	return (0);
}

int	main(int argc, char **argv)
{
	t_stack	*a;
	t_stack	*b;
	int		i;
	int		res;

	a = NULL;
	b = NULL;
	if (argc < 2)
		return (0);
	i = 1;
	while (i < argc)
	{
		if (argv[i][0] == '\0')
		{
			ft_putstr_fd("Error\n", 2);
			return (1);
		}
		i++;
	}
	init_program(argv + 1, &a);
	normalize_indices(a);
	res = run_checker(&a, &b);
	free_stack(&a);
	free_stack(&b);
	return (res);
}
