/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/29 21:54:38 by adarabi           #+#    #+#             */
/*   Updated: 2026/04/29 22:03:54 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putnbr_fd(int n, int fd)
{
	long int	nbr;

	nbr = n;
	if (fd < 0)
		return ;
	if (nbr < 0)
	{
		ft_putchar_fd('-', fd);
		nbr = -nbr;
	}
	if (nbr >= 10)
		ft_putnbr_fd(nbr / 10, fd);
	ft_putchar_fd((nbr % 10) + '0', fd);
}

// int	main(void)
// {
// 	ft_putstr_fd("Test 42:    ", 1);
// 	ft_putnbr_fd(42, 1);
// 	ft_putchar_fd('\n', 1);
// 	ft_putstr_fd("Test 0:     ", 1);
// 	ft_putnbr_fd(0, 1);
// 	ft_putchar_fd('\n', 1);
// 	ft_putstr_fd("Test -123:  ", 1);
// 	ft_putnbr_fd(-123, 1);
// 	ft_putchar_fd('\n', 1);
// 	ft_putstr_fd("Test MIN:   ", 1);
// 	ft_putnbr_fd(-2147483648, 1);
// 	ft_putchar_fd('\n', 1);
// 	ft_putstr_fd("Test MAX:   ", 1);
// 	ft_putnbr_fd(2147483647, 1);
// 	ft_putchar_fd('\n', 1);
// 	ft_putstr_fd("\nChecking FD 2 (stderr): ", 1);
// 	ft_putnbr_fd(99, 2);
// 	ft_putchar_fd('\n', 1);
// 	return (0);
// }
