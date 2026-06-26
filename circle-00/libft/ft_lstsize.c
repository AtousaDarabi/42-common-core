/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstsize.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/30 13:51:49 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/05 18:54:13 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_lstsize(t_list *lst)
{
	int	count;

	count = 0;
	while (lst)
	{
		count++;
		lst = lst->next;
	}
	return (count);
}

// int	main(void)
// {
// 	t_list	*head;

// 	head = NULL;
// 	ft_lstadd_front(&head, ft_lstnew("First node"));
// 	ft_lstadd_front(&head, ft_lstnew("Second node"));
// 	ft_lstadd_front(&head, ft_lstnew("Third node"));
// 	printf("Size of list: %d\n", ft_lstsize(head));
// 	return (0);
// }
